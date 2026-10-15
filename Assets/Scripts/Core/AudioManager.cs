using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace HalloweenVN.Core
{
    /// <summary>
    /// Central BGM/SFX player.
    /// - Final volume = user slider (SettingsData) x per-clip loudness gain x fade factor.
    /// - Per-clip gains were measured with EBU R128 (ffmpeg ebur128) so that every BGM sits at ~-16 LUFS
    ///   and never exceeds 0 dBTP. Re-measure and update ClipGain when audio files are replaced.
    /// </summary>
    public class AudioManager : MonoBehaviour
    {
        public static AudioManager Instance { get; private set; }

        public const string LobbyBGM = "bgm_lobby";

        [Header("Audio Sources")]
        [SerializeField] private AudioSource bgmSource;
        [SerializeField] private AudioSource sfxSource;
        private AudioSource uiSource;

        // ── Loudness normalization (measured 2026-10-05, target BGM -16 LUFS integrated) ──
        // bgm_climax -12.0 LUFS / +0.6 dBTP, bgm_ending_piano -11.0 / +0.2, bgm_investigation -13.1 / 0.0,
        // bgm_lobby -12.3 / +0.2, bgm_office_day -12.1 / +0.2, bgm_office_night -11.6 / +0.1
        private static readonly Dictionary<string, float> ClipGain = new Dictionary<string, float>
        {
            { "bgm_climax",        0.63f }, // -4.0 dB
            { "bgm_ending_piano",  0.56f }, // -5.0 dB
            { "bgm_investigation", 0.72f }, // -2.9 dB
            { "bgm_lobby",         0.65f }, // -3.7 dB
            { "bgm_office_day",    0.64f }, // -3.9 dB
            { "bgm_office_night",  0.60f }, // -4.4 dB
            { "sfx_heartbeat",     0.85f }, // momentary -13 LUFS: slightly tamed so it doesn't overpower BGM
            { "sfx_ui_click",      1.00f },
            { "sfx_ui_hover",      1.00f },
        };

        // Leading silence to skip (seconds). sfx_heartbeat has ~1.05 s of silence at the head.
        private static readonly Dictionary<string, float> ClipStartOffset = new Dictionary<string, float>
        {
            { "sfx_heartbeat", 1.0f },
        };

        private static float GainOf(string clipName)
        {
            return (clipName != null && ClipGain.TryGetValue(clipName, out float g)) ? g : 1f;
        }

        // ── BGM state ──
        private string currentBgmName;
        private float currentBgmGain = 1f;
        private float bgmFade = 1f;
        private Coroutine bgmCoroutine;

        /// <summary>Name of the BGM that is playing (or about to play). Null when stopped.</summary>
        public string CurrentBGM => currentBgmName;

        // ── SFX state ──
        private readonly Dictionary<string, AudioClip> sfxCache = new Dictionary<string, AudioClip>();
        private readonly HashSet<string> pendingSfx = new HashSet<string>();
        private int sfxGeneration;

        private class TimedSfx
        {
            public string name;
            public AudioSource source;
            public float gain;
            public float fade = 1f;
            public Coroutine routine;
        }
        private readonly List<TimedSfx> timedSfx = new List<TimedSfx>();

        private void Awake()
        {
            if (Instance == null)
            {
                Instance = this;
                DontDestroyOnLoad(gameObject);
                InitializeSources();
            }
            else
            {
                Destroy(this);
            }
        }

        private IEnumerator Start()
        {
            // GameManager is created by HalloweenUIBuilder; wait until it exists.
            float waited = 0f;
            while (GameManager.Instance == null && waited < 5f)
            {
                waited += Time.unscaledDeltaTime;
                yield return null;
            }
            if (GameManager.Instance == null) yield break;

            GameManager.Instance.OnPhaseChanged += HandlePhaseChanged;

            // The game boots in the Lobby phase without firing OnPhaseChanged,
            // so the lobby music has to be started here (first launch).
            if (GameManager.Instance.CurrentPhase == GamePhase.Lobby && string.IsNullOrEmpty(currentBgmName))
            {
                PlayBGM(LobbyBGM, 1.5f);
            }
        }

        private void OnDestroy()
        {
            if (Instance == this && GameManager.Instance != null)
                GameManager.Instance.OnPhaseChanged -= HandlePhaseChanged;
        }

        private void Update()
        {
            // WebGL autoplay recovery: if a BGM track is supposed to be playing (and not mid-transition),
            // but the browser blocked AudioSource.Play() prior to the first user gesture, start it on interaction.
            if (!string.IsNullOrEmpty(currentBgmName) && bgmCoroutine == null && bgmSource != null && bgmSource.clip != null && !bgmSource.isPlaying)
            {
                bool userInteracted =
                    (UnityEngine.InputSystem.Mouse.current != null &&
                     (UnityEngine.InputSystem.Mouse.current.leftButton.wasPressedThisFrame ||
                      UnityEngine.InputSystem.Mouse.current.rightButton.wasPressedThisFrame)) ||
                    (UnityEngine.InputSystem.Keyboard.current != null && UnityEngine.InputSystem.Keyboard.current.anyKey.wasPressedThisFrame) ||
                    (UnityEngine.InputSystem.Touchscreen.current != null && UnityEngine.InputSystem.Touchscreen.current.primaryTouch.press.wasPressedThisFrame);

                if (userInteracted && bgmSource.clip.loadState == AudioDataLoadState.Loaded)
                {
                    ApplyBgmVolume();
                    bgmSource.Play();
                }
            }
        }

        private void HandlePhaseChanged(GamePhase phase)
        {
            if (phase == GamePhase.Lobby)
            {
                StopAllSFX();
                PlayBGM(LobbyBGM);
            }
        }

        private void InitializeSources()
        {
            if (bgmSource == null)
            {
                bgmSource = gameObject.AddComponent<AudioSource>();
                bgmSource.loop = true;
                bgmSource.playOnAwake = false;
                bgmSource.spatialBlend = 0f;
            }
            if (sfxSource == null)
            {
                sfxSource = gameObject.AddComponent<AudioSource>();
                sfxSource.loop = false;
                sfxSource.playOnAwake = false;
                sfxSource.spatialBlend = 0f;
            }
            if (uiSource == null)
            {
                uiSource = gameObject.AddComponent<AudioSource>();
                uiSource.loop = false;
                uiSource.playOnAwake = false;
                uiSource.spatialBlend = 0f;
            }
            uiSource.pitch = 1.0f;
            uiSource.volume = 1f;
            sfxSource.volume = 1f;

            // Preload critical UI sounds so first click is instantaneous
            LoadSFX("sfx_ui_click");
            LoadSFX("sfx_ui_hover");

            UpdateVolume();
        }

        /// <summary>Re-applies slider values to everything that is currently playing.</summary>
        public void UpdateVolume()
        {
            ApplyBgmVolume();
            foreach (var t in timedSfx)
            {
                if (t.source != null) t.source.volume = SettingsData.SFXVolume * t.gain * t.fade;
            }
        }

        private void ApplyBgmVolume()
        {
            if (bgmSource != null)
                bgmSource.volume = Mathf.Clamp01(SettingsData.BGMVolume * currentBgmGain * bgmFade);
        }

        // ═══════════════ BGM ═══════════════

        public void PlayBGM(string trackName, float fadeDuration = 1.0f)
        {
            if (string.IsNullOrEmpty(trackName)) return;

            // Same track already playing (or fading in) → nothing to do.
            if (trackName == currentBgmName && bgmSource.clip != null && bgmSource.isPlaying) return;

            AudioClip clip = Resources.Load<AudioClip>($"Audio/BGM/{trackName}");
            if (clip == null)
            {
                Debug.LogWarning($"[AudioManager] BGM not found: Audio/BGM/{trackName}");
                return;
            }

            currentBgmName = trackName;
            if (bgmCoroutine != null) StopCoroutine(bgmCoroutine);
            bgmCoroutine = StartCoroutine(SwitchBGM(clip, GainOf(trackName), fadeDuration));
        }

        public void StopBGM(float fadeDuration = 1.0f)
        {
            currentBgmName = null;
            if (bgmCoroutine != null) StopCoroutine(bgmCoroutine);
            bgmCoroutine = StartCoroutine(FadeOutAndStopBGM(fadeDuration));
        }

        private IEnumerator SwitchBGM(AudioClip newClip, float newGain, float duration)
        {
            yield return WaitForAudioData(newClip);
            if (newClip == null || newClip.loadState != AudioDataLoadState.Loaded)
            {
                currentBgmName = bgmSource.clip != null ? bgmSource.clip.name : null;
                bgmCoroutine = null;
                yield break;
            }
            float half = Mathf.Max(0.01f, duration * 0.5f);

            if (bgmSource.isPlaying && bgmSource.clip != null && bgmFade > 0f)
            {
                yield return FadeBgm(0f, half);
            }

            AudioClip oldClip = bgmSource.clip;
            bgmSource.Stop();
            bgmSource.clip = newClip;
            currentBgmGain = newGain;
            bgmFade = 0f;
            ApplyBgmVolume();
            bgmSource.Play();

            // Free the decoded data of the previous track (each BGM is ~3 min of audio).
            if (oldClip != null && oldClip != newClip) Resources.UnloadAsset(oldClip);

            yield return FadeBgm(1f, half);
            bgmCoroutine = null;
        }

        private IEnumerator FadeOutAndStopBGM(float duration)
        {
            yield return FadeBgm(0f, Mathf.Max(0.01f, duration));
            AudioClip oldClip = bgmSource.clip;
            bgmSource.Stop();
            bgmSource.clip = null;
            if (oldClip != null) Resources.UnloadAsset(oldClip);
            bgmCoroutine = null;
        }

        private IEnumerator FadeBgm(float target, float duration)
        {
            float start = bgmFade;
            float t = 0f;
            while (t < duration)
            {
                t += Time.unscaledDeltaTime;
                bgmFade = Mathf.Lerp(start, target, t / duration);
                ApplyBgmVolume();
                yield return null;
            }
            bgmFade = target;
            ApplyBgmVolume();
        }

        // ═══════════════ SFX ═══════════════

        /// <summary>
        /// Plays a sound effect. If maxDuration &gt; 0 the sound is faded out over fadeOutTime
        /// so that it is completely silent at maxDuration seconds.
        /// </summary>
        public void PlaySFX(string sfxName, float maxDuration = 0f, float fadeOutTime = 1f)
        {
            if (string.IsNullOrEmpty(sfxName)) return;
            AudioClip clip = LoadSFX(sfxName);
            if (clip == null) return;

            float gain = GainOf(sfxName);
            float offset = ClipStartOffset.TryGetValue(sfxName, out float o) ? o : 0f;
            bool isTimed = (maxDuration > 0f || offset > 0f);

            // For timed/ambient SFX (like heartbeat), prevent rapid re-triggering while loading
            if (isTimed && !pendingSfx.Add(sfxName)) return;

            // If audio data is already loaded and it's a standard one-shot, play immediately with 0 latency!
            if (!isTimed && clip.loadState == AudioDataLoadState.Loaded)
            {
                if (sfxName.StartsWith("sfx_ui_"))
                {
                    if (uiSource != null) uiSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
                }
                else
                {
                    if (sfxSource != null) sfxSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
                }
                return;
            }

            StartCoroutine(PlaySfxWhenReady(sfxName, clip, gain, offset, maxDuration, fadeOutTime, isTimed, sfxGeneration));
        }

        private IEnumerator WaitForAudioData(AudioClip clip)
        {
            if (clip == null) yield break;
            if (clip.loadState == AudioDataLoadState.Unloaded) clip.LoadAudioData();
            float deadline = Time.realtimeSinceStartup + 10f;
            while (clip != null && clip.loadState != AudioDataLoadState.Loaded &&
                   clip.loadState != AudioDataLoadState.Failed && Time.realtimeSinceStartup < deadline)
                yield return null;
            if (clip != null && clip.loadState != AudioDataLoadState.Loaded)
                Debug.LogWarning($"[AudioManager] Audio data could not be loaded: {clip.name}");
        }

        private IEnumerator PlaySfxWhenReady(string sfxName, AudioClip clip, float gain, float offset, float maxDuration, float fadeOutTime, bool isTimed, int generation)
        {
            try
            {
                yield return WaitForAudioData(clip);
                if (generation != sfxGeneration) yield break;
                if (clip == null || clip.loadState != AudioDataLoadState.Loaded) yield break;

                if (isTimed)
                {
                    PlayTimedSFX(sfxName, clip, gain, offset, maxDuration, fadeOutTime);
                }
                else
                {
                    if (sfxName.StartsWith("sfx_ui_"))
                    {
                        if (uiSource != null) uiSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
                    }
                    else
                    {
                        if (sfxSource != null) sfxSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
                    }
                }
            }
            finally
            {
                if (isTimed)
                {
                    pendingSfx.Remove(sfxName);
                }
            }
        }

        private void PlayTimedSFX(string sfxName, AudioClip clip, float gain, float offset, float maxDuration, float fadeOutTime)
        {
            // Never stack the same timed effect (e.g. two heartbeats when skipping quickly).
            for (int i = timedSfx.Count - 1; i >= 0; i--)
            {
                if (timedSfx[i].name == sfxName) StopTimed(timedSfx[i]);
            }

            offset = Mathf.Clamp(offset, 0f, Mathf.Max(0f, clip.length - 0.001f));
            var entry = new TimedSfx { name = sfxName, gain = gain };
            entry.source = gameObject.AddComponent<AudioSource>();
            entry.source.playOnAwake = false;
            entry.source.spatialBlend = 0f;
            entry.source.clip = clip;
            entry.source.volume = SettingsData.SFXVolume * gain;
            if (offset > 0f && offset < clip.length) entry.source.time = offset;
            entry.source.Play();
            timedSfx.Add(entry);

            float length = clip.length - offset;
            float total = maxDuration > 0f ? Mathf.Min(maxDuration, length) : length;
            entry.routine = StartCoroutine(TimedSfxRoutine(entry, total, maxDuration > 0f ? fadeOutTime : 0f));
        }

        private IEnumerator TimedSfxRoutine(TimedSfx entry, float total, float fadeOutTime)
        {
            fadeOutTime = Mathf.Clamp(fadeOutTime, 0f, total);
            float hold = total - fadeOutTime;
            if (hold > 0f) yield return new WaitForSecondsRealtime(hold);

            float t = 0f;
            while (t < fadeOutTime && entry.source != null)
            {
                t += Time.unscaledDeltaTime;
                entry.fade = 1f - Mathf.Clamp01(t / fadeOutTime);
                entry.source.volume = SettingsData.SFXVolume * entry.gain * entry.fade;
                yield return null;
            }

            entry.routine = null;
            StopTimed(entry);
        }

        private void StopTimed(TimedSfx entry)
        {
            if (entry.routine != null) StopCoroutine(entry.routine);
            if (entry.source != null)
            {
                entry.source.Stop();
                Destroy(entry.source);
            }
            timedSfx.Remove(entry);
        }

        /// <summary>Stops every sound effect that is still playing (used on rewind / return to lobby).</summary>
        public void StopAllSFX()
        {
            sfxGeneration++;
            pendingSfx.Clear();
            for (int i = timedSfx.Count - 1; i >= 0; i--) StopTimed(timedSfx[i]);
            if (sfxSource != null) sfxSource.Stop();
            if (uiSource != null) uiSource.Stop();
        }

        private AudioClip LoadSFX(string sfxName)
        {
            if (string.IsNullOrEmpty(sfxName)) return null;
            if (sfxCache.TryGetValue(sfxName, out AudioClip clip)) return clip;
            clip = Resources.Load<AudioClip>($"Audio/SFX/{sfxName}");
            
            if (clip != null) 
            {
                sfxCache[sfxName] = clip;
            }
            else Debug.LogWarning($"[AudioManager] SFX not found: Audio/SFX/{sfxName}");
            return clip;
        }
    }
}

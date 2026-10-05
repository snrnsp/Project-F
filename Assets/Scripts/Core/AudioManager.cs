using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace HalloweenVN.Core
{
    public class AudioManager : MonoBehaviour
    {
        public static AudioManager Instance { get; private set; }

        [Header("Audio Sources")]
        [SerializeField] private AudioSource bgmSource;
        [SerializeField] private AudioSource sfxSource;

        private Dictionary<string, AudioClip> bgmDict = new Dictionary<string, AudioClip>();
        private Dictionary<string, AudioClip> sfxDict = new Dictionary<string, AudioClip>();

        private Coroutine fadeCoroutine;

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
                Destroy(gameObject);
            }
        }

        private void InitializeSources()
        {
            if (bgmSource == null)
            {
                bgmSource = gameObject.AddComponent<AudioSource>();
                bgmSource.loop = true;
                bgmSource.playOnAwake = false;
            }
            if (sfxSource == null)
            {
                sfxSource = gameObject.AddComponent<AudioSource>();
                sfxSource.loop = false;
                sfxSource.playOnAwake = false;
            }

            UpdateVolume();
        }

        public void UpdateVolume()
        {
            if (bgmSource != null)
                bgmSource.volume = SettingsData.BGMVolume;
            if (sfxSource != null)
                sfxSource.volume = SettingsData.SFXVolume;
        }

        public void PlayBGM(string trackName, float fadeDuration = 1.0f)
        {
            AudioClip clip = LoadBGM(trackName);
            if (clip == null) return;

            if (bgmSource.clip == clip && bgmSource.isPlaying) return;

            if (fadeCoroutine != null) StopCoroutine(fadeCoroutine);
            fadeCoroutine = StartCoroutine(CrossfadeBGM(clip, fadeDuration));
        }

        public void StopBGM(float fadeDuration = 1.0f)
        {
            if (fadeCoroutine != null) StopCoroutine(fadeCoroutine);
            fadeCoroutine = StartCoroutine(FadeOutBGM(fadeDuration));
        }

        public void PlaySFX(string sfxName)
        {
            AudioClip clip = LoadSFX(sfxName);
            if (clip != null)
            {
                sfxSource.PlayOneShot(clip, SettingsData.SFXVolume);
            }
        }

        private AudioClip LoadBGM(string trackName)
        {
            if (bgmDict.TryGetValue(trackName, out AudioClip clip)) return clip;
            clip = Resources.Load<AudioClip>($"Audio/BGM/{trackName}");
            if (clip != null) bgmDict[trackName] = clip;
            else Debug.LogWarning($"[AudioManager] BGM not found: Audio/BGM/{trackName}");
            return clip;
        }

        private AudioClip LoadSFX(string sfxName)
        {
            if (sfxDict.TryGetValue(sfxName, out AudioClip clip)) return clip;
            clip = Resources.Load<AudioClip>($"Audio/SFX/{sfxName}");
            if (clip != null) sfxDict[sfxName] = clip;
            else Debug.LogWarning($"[AudioManager] SFX not found: Audio/SFX/{sfxName}");
            return clip;
        }

        private IEnumerator CrossfadeBGM(AudioClip newClip, float duration)
        {
            float targetVolume = SettingsData.BGMVolume;
            
            // Fade out current if playing
            if (bgmSource.isPlaying)
            {
                float startVolume = bgmSource.volume;
                for (float t = 0; t < duration / 2; t += Time.unscaledDeltaTime)
                {
                    bgmSource.volume = Mathf.Lerp(startVolume, 0, t / (duration / 2));
                    yield return null;
                }
                bgmSource.volume = 0;
            }

            bgmSource.clip = newClip;
            bgmSource.Play();

            // Fade in new
            for (float t = 0; t < duration / 2; t += Time.unscaledDeltaTime)
            {
                bgmSource.volume = Mathf.Lerp(0, targetVolume, t / (duration / 2));
                yield return null;
            }
            bgmSource.volume = targetVolume;
        }

        private IEnumerator FadeOutBGM(float duration)
        {
            float startVolume = bgmSource.volume;
            for (float t = 0; t < duration; t += Time.unscaledDeltaTime)
            {
                bgmSource.volume = Mathf.Lerp(startVolume, 0, t / duration);
                yield return null;
            }
            bgmSource.volume = 0;
            bgmSource.Stop();
            bgmSource.clip = null;
        }
    }
}

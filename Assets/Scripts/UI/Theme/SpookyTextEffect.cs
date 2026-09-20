using UnityEngine;
using TMPro;
using System.Collections;
using System;
using Random = UnityEngine.Random;

namespace HalloweenVN.UI.Theme
{
    public enum EffectType
    {
        None,
        Shake,
        Wave,
        Tremble,
        FadeInPerChar,
        Glitch
    }

    [RequireComponent(typeof(TextMeshProUGUI))]
    public class SpookyTextEffect : MonoBehaviour
    {
        [SerializeField] private EffectType currentEffect = EffectType.None;
        [SerializeField] private float shakeIntensity = 2f;
        [SerializeField] private float waveAmplitude = 5f;
        [SerializeField] private float waveFrequency = 3f;
        [SerializeField] private float trembleSpeed = 20f;
        [SerializeField] private float glitchInterval = 0.1f;

        private TextMeshProUGUI textComponent;
        private bool isAnimating;
        private Coroutine effectCoroutine;
        private float nextGlitchTime;
        private float fadeInProgress;

        private void Awake()
        {
            textComponent = GetComponent<TextMeshProUGUI>();
        }

        private void OnEnable()
        {
            isAnimating = true;
            fadeInProgress = 0f;
        }

        private void OnDisable()
        {
            isAnimating = false;
        }

        private void Update()
        {
            if (!isAnimating || currentEffect == EffectType.None) return;
            if (string.IsNullOrEmpty(textComponent.text)) return;

            textComponent.ForceMeshUpdate();
            TMP_TextInfo textInfo = textComponent.textInfo;

            if (textInfo.characterCount == 0) return;
            
            if (currentEffect == EffectType.FadeInPerChar)
            {
                fadeInProgress += Time.deltaTime * 5f; // Example speed
            }

            for (int i = 0; i < textInfo.characterCount; i++)
            {
                if (!textInfo.characterInfo[i].isVisible) continue;

                int vertexIndex = textInfo.characterInfo[i].vertexIndex;
                int materialIndex = textInfo.characterInfo[i].materialReferenceIndex;
                Vector3[] vertices = textInfo.meshInfo[materialIndex].vertices;
                Color32[] colors = textInfo.meshInfo[materialIndex].colors32;

                Vector3 offset = Vector3.zero;

                switch (currentEffect)
                {
                    case EffectType.Shake:
                        offset = new Vector3(Random.Range(-shakeIntensity, shakeIntensity), Random.Range(-shakeIntensity, shakeIntensity), 0);
                        break;
                    case EffectType.Tremble:
                        float trembleX = Mathf.PerlinNoise(Time.time * trembleSpeed, i) * 2f - 1f;
                        float trembleY = Mathf.PerlinNoise(i, Time.time * trembleSpeed) * 2f - 1f;
                        offset = new Vector3(trembleX, trembleY, 0) * (shakeIntensity * 0.5f);
                        break;
                    case EffectType.Wave:
                        offset = new Vector3(0, Mathf.Sin(Time.time * waveFrequency + i) * waveAmplitude, 0);
                        break;
                    case EffectType.Glitch:
                        if (Time.time > nextGlitchTime && Random.value > 0.8f)
                        {
                            offset = new Vector3(Random.Range(-shakeIntensity * 2, shakeIntensity * 2), Random.Range(-shakeIntensity * 2, shakeIntensity * 2), 0);
                            for (int j = 0; j < 4; j++)
                            {
                                colors[vertexIndex + j] = new Color32((byte)Random.Range(0, 255), (byte)Random.Range(0, 255), (byte)Random.Range(0, 255), 255);
                            }
                        }
                        break;
                    case EffectType.FadeInPerChar:
                        float charAlpha = Mathf.Clamp01(fadeInProgress - i * 0.1f);
                        for (int j = 0; j < 4; j++)
                        {
                            colors[vertexIndex + j].a = (byte)(charAlpha * 255);
                        }
                        break;
                }

                if (offset != Vector3.zero)
                {
                    vertices[vertexIndex + 0] += offset;
                    vertices[vertexIndex + 1] += offset;
                    vertices[vertexIndex + 2] += offset;
                    vertices[vertexIndex + 3] += offset;
                }
            }

            if (currentEffect == EffectType.Glitch && Time.time > nextGlitchTime)
            {
                nextGlitchTime = Time.time + glitchInterval;
            }

            textComponent.UpdateVertexData(TMP_VertexDataUpdateFlags.All);
        }

        /// <summary>
        /// Changes the current visual effect.
        /// </summary>
        /// <param name="effect">The effect type to apply.</param>
        public void SetEffect(EffectType effect)
        {
            if (currentEffect != effect && effect == EffectType.FadeInPerChar)
            {
                fadeInProgress = 0f;
            }
            currentEffect = effect;
            isAnimating = currentEffect != EffectType.None;
            if (!isAnimating)
            {
                textComponent.ForceMeshUpdate(); // Reset
            }
        }

        /// <summary>
        /// Stops the current effect and resets the text mesh.
        /// </summary>
        public void StopEffect()
        {
            SetEffect(EffectType.None);
        }

        /// <summary>
        /// Plays a specific effect for a given duration, then stops it.
        /// </summary>
        /// <param name="effect">The effect to play.</param>
        /// <param name="duration">Duration in seconds.</param>
        public void PlayEffect(EffectType effect, float duration)
        {
            if (effectCoroutine != null) StopCoroutine(effectCoroutine);
            effectCoroutine = StartCoroutine(PlayEffectCoroutine(effect, duration));
        }

        private IEnumerator PlayEffectCoroutine(EffectType effect, float duration)
        {
            SetEffect(effect);
            yield return new WaitForSeconds(duration);
            StopEffect();
        }

        /// <summary>
        /// Applies a one-shot shake effect to any TextMeshProUGUI component.
        /// </summary>
        /// <param name="text">The text component to shake.</param>
        /// <param name="intensity">The intensity of the shake.</param>
        public static void ApplyShakeToText(TextMeshProUGUI text, float intensity)
        {
            if (text == null) return;
            text.ForceMeshUpdate();
            var textInfo = text.textInfo;

            for (int i = 0; i < textInfo.characterCount; i++)
            {
                if (!textInfo.characterInfo[i].isVisible) continue;

                int vertexIndex = textInfo.characterInfo[i].vertexIndex;
                int materialIndex = textInfo.characterInfo[i].materialReferenceIndex;
                Vector3[] vertices = textInfo.meshInfo[materialIndex].vertices;

                Vector3 offset = new Vector3(Random.Range(-intensity, intensity), Random.Range(-intensity, intensity), 0);

                vertices[vertexIndex + 0] += offset;
                vertices[vertexIndex + 1] += offset;
                vertices[vertexIndex + 2] += offset;
                vertices[vertexIndex + 3] += offset;
            }

            text.UpdateVertexData(TMP_VertexDataUpdateFlags.All);
        }
    }
}

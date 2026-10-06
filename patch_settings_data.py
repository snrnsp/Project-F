import re

with open('Assets/Scripts/Core/SettingsData.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Add EnableFlashingEffects property
if "EnableFlashingEffects" not in content:
    content = content.replace(
        "public static GameLanguage Language { get; set; } = GameLanguage.Korean;",
        "public static GameLanguage Language { get; set; } = GameLanguage.Korean;\n        public static bool EnableFlashingEffects { get; set; } = true;"
    )

    # Add to Load
    content = content.replace(
        "Language = (GameLanguage)PlayerPrefs.GetInt(Prefix + \"Language\", 0);",
        "Language = (GameLanguage)PlayerPrefs.GetInt(Prefix + \"Language\", 0);\n            EnableFlashingEffects = PlayerPrefs.GetInt(Prefix + \"EnableFlashingEffects\", 1) == 1;"
    )

    # Add to Save
    content = content.replace(
        "PlayerPrefs.SetInt(Prefix + \"Language\", (int)Language);",
        "PlayerPrefs.SetInt(Prefix + \"Language\", (int)Language);\n            PlayerPrefs.SetInt(Prefix + \"EnableFlashingEffects\", EnableFlashingEffects ? 1 : 0);"
    )

    # Add to ResetToDefaults
    content = content.replace(
        "PerformanceMode = 1;",
        "PerformanceMode = 1;\n            EnableFlashingEffects = true;"
    )

    with open('Assets/Scripts/Core/SettingsData.cs', 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Patched SettingsData.cs")
else:
    print("Already patched or could not find hooks.")

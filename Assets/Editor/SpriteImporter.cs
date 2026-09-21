#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

namespace HalloweenVN.Editor
{
    public class SpriteImporter : AssetPostprocessor
    {
        void OnPreprocessTexture()
        {
            if (assetPath.Contains("Assets/Resources/Characters"))
            {
                TextureImporter textureImporter = (TextureImporter)assetImporter;
                if (textureImporter.textureType != TextureImporterType.Sprite)
                {
                    textureImporter.textureType = TextureImporterType.Sprite;
                    textureImporter.spriteImportMode = SpriteImportMode.Single;
                    textureImporter.alphaIsTransparency = true;
                    textureImporter.mipmapEnabled = false;
                }
            }
        }

        [MenuItem("Tools/Reimport Characters as Sprites")]
        public static void ReimportCharacters()
        {
            AssetDatabase.ImportAsset("Assets/Resources/Characters", ImportAssetOptions.ImportRecursive);
            Debug.Log("✅ Characters reimported as sprites!");
        }
    }
}
#endif

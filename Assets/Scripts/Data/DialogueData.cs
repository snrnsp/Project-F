using System.Collections.Generic;

namespace HalloweenVN.Data
{
    [System.Serializable]
    public class DialogueChoice
    {
        public string text;
        public string text_en;
        public string text_ja;
        public string text_cn;
        public string text_tw;
        public int nextNodeId;
    }

    [System.Serializable]
    public class DialogueNode
    {
        public int id;
        public string speaker;
        public string text;
        public string text_en;
        public string text_ja;
        public string text_cn;
        public string text_tw;
        public string characterSprite; // Legacy / Default (maps to Center)
        public string characterSpriteLeft;
        public string characterSpriteCenter;
        public string characterSpriteRight;
        public string backgroundSprite;
        public List<DialogueChoice> choices;
        public int nextNodeId;
        public string command;
        public bool noFade; // If true, character appears instantly without fade animation
        public bool slideIn; // If true, character slides into their position
        public bool slideFromRight; // If true, overrides default slide direction for Center
    }

    [System.Serializable]
    public class DialogueContainer
    {
        public string dialogueId;
        // Music inherited at chapter entry, also used when reading older saves.
        public string initialBgm;
        public List<DialogueNode> nodes;
    }
}

using System.Collections.Generic;

namespace HalloweenVN.Data
{
    [System.Serializable]
    public class DialogueChoice
    {
        public string text;
        public int nextNodeId;
    }

    [System.Serializable]
    public class DialogueNode
    {
        public int id;
        public string speaker;
        public string text;
        public string characterSprite; // Legacy / Default (maps to Center)
        public string characterSpriteLeft;
        public string characterSpriteCenter;
        public string characterSpriteRight;
        public string backgroundSprite;
        public List<DialogueChoice> choices;
        public int nextNodeId;
        public string command;
    }

    [System.Serializable]
    public class DialogueContainer
    {
        public string dialogueId;
        public List<DialogueNode> nodes;
    }
}

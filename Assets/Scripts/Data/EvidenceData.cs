using System.Collections.Generic;

namespace HalloweenVN.Data
{
    [System.Serializable]
    public class EvidenceInfo
    {
        public string id;
        public string evidenceName;
        public string description;
        public string iconPath;
    }

    [System.Serializable]
    public class EvidenceDatabase
    {
        public List<EvidenceInfo> evidences;
    }
}

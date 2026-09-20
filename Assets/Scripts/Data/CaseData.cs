using System.Collections.Generic;

namespace HalloweenVN.Data
{
    [System.Serializable]
    public class CaseQuestion
    {
        public string questionText;
        public string correctEvidenceId;
    }

    [System.Serializable]
    public class CaseContainer
    {
        public string caseId;
        public string caseName;
        public List<CaseQuestion> questions;
        public string perfectDialogueId;
        public string failDialogueId;
    }
}

using System;
using System.IO;
using System.Text;

class Program {
    static void Main() {
        string path = @"Assets\Scripts\UI\LobbyUI.cs";
        string content = File.ReadAllText(path, new UTF8Encoding(false));
        
        string target1 = "            }\r\n        private void Start()";
        string target2 = "            }\n        private void Start()";
        string target3 = "            }\r\n\r\n        private void Start()";
        
        string rep = "            }\n        }\n\n        private void Start()";
        
        if (content.Contains(target1)) {
            content = content.Replace(target1, rep);
        } else if (content.Contains(target2)) {
            content = content.Replace(target2, rep);
        } else if (content.Contains(target3)) {
            content = content.Replace(target3, rep);
        } else {
            Console.WriteLine("NOT FOUND");
        }
        
        File.WriteAllText(path, content, new UTF8Encoding(true));
        Console.WriteLine("SUCCESS");
    }
}

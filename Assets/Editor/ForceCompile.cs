using UnityEditor;
public class ForceCompile {
    [MenuItem("Tools/Force Recompile")]
    public static void DoCompile() {
        UnityEditor.Compilation.CompilationPipeline.RequestScriptCompilation();
    }
}

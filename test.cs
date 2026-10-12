using System;
using System.Collections.Generic;

public class Test
{
    public static void Main()
    {
        string[] owner = { "카스미", "미나", "세이카" };
        float[] result = { 0.25f, 0.5f, 0.75f };
        List<int> used = new List<int>();
        for (int s = 0; s < 3; s++) if (owner[s] != null) used.Add(s);
        float[] xs;
        if (used.Count == 1) xs = new float[] { 0.5f };
        else if (used.Count == 2) xs = new float[] { 0.25f, 0.75f };
        else xs = new float[] { 0.20f, 0.50f, 0.80f };
        
        for (int i = 0; i < used.Count; i++)
        {
            int s = used[i];
            float target = xs[i];
            
            if (owner[s] == "리나")
            {
                if (target < 0.5f) target += 0.05f;
                else if (target > 0.5f) target -= 0.05f;
            }
            
            result[s] = target;
        }
        
        Console.WriteLine("0: " + result[0] + ", 1: " + result[1] + ", 2: " + result[2]);
    }
}

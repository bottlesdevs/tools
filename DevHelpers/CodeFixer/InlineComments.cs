using System;
using System.IO;
using System.Text.RegularExpressions;

namespace CodeFixer
{    
    public class InlineComments
    {
        public bool LastResult = false;

        // costruttori
        public InlineComments(){}
        public InlineComments(string path, bool isFile = false)
        {
            if(isFile) {
                ProcessFile(path);
                return;
            }
            ProcessDirectory(path);
        }

        public bool ProcessDirectory(string directory)
        {
            if (!Directory.Exists(directory))
            {
                Console.WriteLine("Directory {0} does not exist", directory);
                LastResult = false;
                return false;
            }
            string[] files = Directory.GetFiles(directory, "*.py");
            foreach (string file in files)
            {
                Console.WriteLine("Processing {0}", file);
                ProcessFile(file);
            }

            LastResult = true;
            return true;
        }

        void ProcessFile(string file)
        {
            string content = File.ReadAllText(file);
            string newContent = Regex.Replace(
                content, 
                @"'''(.+?)'''",
                m => "# " + m.Groups[1].Value
            );
            if (newContent != content)
            {
                File.WriteAllText(file, newContent);
            }
        }

    }
}

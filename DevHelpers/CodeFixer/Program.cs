using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace CodeFixer
{
    
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 0) return;
            string toolName = args[0];
            string directory = string.Empty;

            if(args.Length > 1) {
                directory = args[1];
            }

            // create a dictionary with 3 example keys
            var man = new Dictionary<string, string>();
            man.Add(
                "help", 
                "Show this help menu."
            );
            man.Add(
                "inline-comments", 
                "Replace comment blocks ('''...''') with inline comments (# ...) " + 
                "in all Python files from a givven directory."
            );
            man.Add(
                "optimize-imports", 
                "Optimize imports in all Python files from a givven directory."
            );

            switch (toolName)
            {
                case "help":
                    foreach (var doc in man)
                    {
                        Console.WriteLine($"{doc.Key} - {doc.Value}");
                    }
                    break;

                case "inline-comments":
                    new InlineComments(directory);
                    break;

                case "optimize-imports":
                    Console.WriteLine("To be implemented ..");
                    break;
                    
                default:
                    Console.WriteLine("Unknown tool name: " + toolName);
                    Console.WriteLine("Usage: CodeFixer.dll <toolName> <directory>");
                    break;
            }
        }
    }
}

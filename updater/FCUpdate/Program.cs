using System;
using System.Diagnostics;
using System.ComponentModel;
using System.Linq;
using System.Net;
using System.IO;

namespace FCUpdate
{

    class ProcessList
    {
        public void FindRunningFinalCif(string[] args)
        // Search and destroy FinalCif.
        {
            string version = args[0];
            Console.WriteLine(args);
            Console.WriteLine("FinalCif Updater");
            Console.WriteLine("Fetching update from server...");

            Process[] processList = Process.GetProcessesByName("FinalCif");
            if (processList.Length > 0) {
                KillProcesses(processList);
            } else
            {
                Console.WriteLine("No running FinalCif process found.");
            }
            string tmp = "C:\\Users\\daniel\\AppData\\Local\\Temp\\tmpDCB3.tmp";
            Console.WriteLine(Path.GetDirectoryName(tmp));
            //string filename = DownloadUpdateFile(version);
            //RunDownloadedFile(filename);
            //DeleteUpdateFile(filename);
        }

        private void DeleteUpdateFile(string file)
        {
            File.Delete(file);
        }

        private void RunDownloadedFile(string file)
        {
            //Process.Start(string.Format("FinalCif-setup-x64-v{0}.exe", version));
            Process.Start(file);
        }

        public void KillProcesses(Process[] processList) 
        // Kills all FinalCif processes
        {
            int i = 1;
            foreach (var process in processList)
            {
                //Console.WriteLine("Process: " + process);
                Console.WriteLine("Ending process {0}: {1}", i, process.ToString().Split()[1]);
                process.Kill();
                i++;
            }
        }

        public string DownloadUpdateFile(string version)
        {

            string dlurl = string.Format("https://xs3-data.uni-freiburg.de/finalcif/FinalCif-setup-x64-v{0}.exe", version);
            string tempdir = Path.GetTempPath();
            string tempfile = Path.GetTempFileName();
            //string combitemp = Path.Combine(tempdir, tempfile);

            //Console.WriteLine("Downloading to: {0}", Path.Combine(tempfile, string.Format("FinalCif-setup-x64-v{0}.exe", version)));
            Console.WriteLine("Downloading to: {0}", tempfile);
            bool erg = false;
            using (var client = new WebClient())
            {
                client.DownloadFile(dlurl, tempfile);
            }

            File.Move(tempfile, Path.GetDirectoryName(tempfile));
            return tempfile;
        } 
           
    }




    class Program
    {
        private static void Main(string[] args)
        {
           ProcessList p = new ProcessList();
            p.FindRunningFinalCif(args);
        }
    }
}



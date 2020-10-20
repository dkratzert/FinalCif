using System;
using System.Net;
using System.IO;
using System.Diagnostics;
using CommandLine;


namespace FCUpdate
{

    class Updater
    {
        const string download_url = "https://xs3-data.uni-freiburg.de/finalcif/FinalCif-setup-x64-v{0}.exe";
        const string setup_name = "FinalCif-setup-x64-v{0}.exe";

        public class Options
        {
            [Option('v', "version", Required = true, HelpText = "Update FinalCif to this version.")]
            public string Version { get; set; }
        }

        public void FindRunningFinalCif(string version)
        // Search and destroy FinalCif.
        {
            Console.WriteLine("FinalCif Updater");
            Console.WriteLine("Fetching update from server...");
            Console.WriteLine($"OS Platform: {Environment.OSVersion.Platform}");

            System.Diagnostics.Process[] processList = Process.GetProcessesByName("FinalCif");
            if (processList.Length > 0) {
                KillProcesses(processList);
            } else
            {
                Console.WriteLine("No running FinalCif process found.");
            }
            string tmp = "C:\\Users\\daniel\\AppData\\Local\\Temp\\tmpDCB3.tmp";
            Console.WriteLine(Path.GetDirectoryName(tmp));
            string filename = DownloadUpdateFile(version);
            int exit_code = RunDownloadedFile(filename);
            Console.WriteLine("exit code: {0}", exit_code);
            DeleteUpdateFile(filename);
        }

        private void DeleteUpdateFile(string file)
        {
            File.Delete(file);
        }

        private int RunDownloadedFile(string file)
        {
            var process = Process.Start(file);
            process.WaitForExit();
            return process.ExitCode;
        }

        private void KillProcesses(Process[] processList)
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

        private string DownloadUpdateFile(string version)
        {

            string dlurl = string.Format(download_url, version);

            string tempfile = Path.GetTempFileName();
            //string combitemp = Path.Combine(tempdir, tempfile);

            //Console.WriteLine("Downloading to: {0}", Path.Combine(tempfile, string.Format("FinalCif-setup-x64-v{0}.exe", version)));
            Console.WriteLine("Downloading to: {0}", tempfile);

            using (var client = new WebClient())
            {
                client.DownloadFile(dlurl, tempfile);
            }
            string tempdir = Path.GetDirectoryName(tempfile);
            string exe_file = Path.Combine(tempdir, string.Format(setup_name, version));
            File.Move(tempfile, exe_file);
            return exe_file;
        }


        private static void Main(params string[] args)
        {

            Parser.Default.ParseArguments<Options>(args)
                   .WithParsed<Options>(o =>
                   {
                       if (o.Version.Length > 0)
                       {
                           Updater u = new Updater();
                           Console.WriteLine($"Version to update: -v {o.Version}");
                           Console.WriteLine("Starting update");
                           u.FindRunningFinalCif(o.Version);
                       }
                       else
                       {
                           Console.WriteLine("Unable to update without version number argument");
                       
                       }
                   });
        }
    }
}



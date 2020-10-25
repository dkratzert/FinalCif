using System;
using System.Net;
using System.IO;
using System.Diagnostics;
using CommandLine;


namespace FCUpdate
{
    class Updater
    {
        //const string download_url = "https://xs3-data.uni-freiburg.de/finalcif/FinalCif-setup-x64-v{0}.exe";
        //const string setup_name = "FinalCif-setup-x64-v{0}.exe";

        public class Options
        {
            [Option('v', "version", Required = true, HelpText = "Update FinalCif to this version.")]
            public string Version { get; set; }
        }

        private static string GetDownloadUrl()
        {
            // MacOSX
            // Unix
            // Win32NT
            var downloadUrl = "empty";
            if (Environment.OSVersion.Platform.ToString().StartsWith("Win"))
            {
                downloadUrl = "https://xs3-data.uni-freiburg.de/finalcif/FinalCif-setup-x64-v{0}.exe";
            }

            if (Environment.OSVersion.Platform.ToString().StartsWith("Unix")) // Find a more specific way for MacOS
            {
                downloadUrl = "https://xs3-data.uni-freiburg.de/finalcif/Finalcif-v{0}_macos.app.zip";
            }

            return downloadUrl;
        }

        private string GetSetupName()
        {
            string setup_name = "no_setup_name";
            if (Environment.OSVersion.Platform.ToString().StartsWith("Win"))
            {
                setup_name = "FinalCif-setup-x64-v{0}.exe";
            }

            if (Environment.OSVersion.Platform.ToString().StartsWith("Unix"))
            {
                setup_name = "Finalcif-v{0}_macos.app.zip";
            }

            return setup_name;
        }

        public void UpdateRunningFinalCifTo(string version)
            // Search and destroy FinalCif.
        {
            ShowStartInfo();
            KillFinalCifProcesses();
            string installerFilename = DownloadUpdate(version);
            int exitCode = RunUpdateInstaller(installerFilename);
            Console.WriteLine("exit code: {0}", exitCode);
            // DeleteUpdateFile(installerFilename);
        }

        private void KillFinalCifProcesses()
        {
            System.Diagnostics.Process[] processList = Process.GetProcessesByName("FinalCif");
            if (processList.Length > 0)
            {
                KillProcesses(processList);
            }
            else
            {
                Console.WriteLine("No running FinalCif process found.");
            }
        }

        private static void ShowStartInfo()
        {
            Console.WriteLine("FinalCif Updater");
            Console.WriteLine("Fetching update from server...");
            Console.WriteLine($"OS Platform: {Environment.OSVersion.Platform}");
        }

        private void DeleteUpdateFile(string file)
        {
            File.Delete(file);
        }

        private int RunUpdateInstaller(string file)
        {
            try
            {
                var process = Process.Start(file);
                if (process != null)
                {
                    process.WaitForExit();
                    return process.ExitCode;
                }
            }
            catch (Exception e)
            {
                //Console.WriteLine(e);
                Console.WriteLine("Unable to run updater");
                //throw;
                return 0;
            }

            return 0;
        }

        private void KillProcesses(Process[] processList)
            // Kills all FinalCif processes
        {
            var i = 1;
            foreach (var process in processList)
            {
                //Console.WriteLine("Process: " + process);
                Console.WriteLine("Ending process {0}: {1}", i, process.ToString().Split()[1]);
                process.Kill();
                i++;
            }
        }

        private string DownloadUpdate(string version)
        {
            Console.WriteLine("download url: {0}", GetDownloadUrl());
            string downloadUrl = string.Format(GetDownloadUrl(), version);
            string tempFile = Path.GetTempFileName();
            Console.WriteLine("Downloading to: {0}", tempFile);
            using (var client = new WebClient())
            {
                client.DownloadFile(downloadUrl, tempFile);
            }

            string exeFile = MoveTempToExeFile(version, tempFile);
            return exeFile;
        }

        private string MoveTempToExeFile(string version, string tempfile)
        {
            string setupName = GetSetupName();
            //string tempdir = Path.GetDirectoryName(tempfile);
            string targetDir = Directory.GetCurrentDirectory();
            //Console.WriteLine(target_dir);
            string filename = string.Format(setupName, version);
            //Console.WriteLine(filename);
            //Console.WriteLine(tempfile);
            string exeFile = Path.Combine(targetDir, filename);
            Console.WriteLine("Move to exe file: {0}", exeFile);
            File.Move(tempfile, exeFile, true);
            return exeFile;
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
                        u.UpdateRunningFinalCifTo(o.Version);
                        Console.WriteLine("Update finished!");
                    }
                    else
                    {
                        Console.WriteLine("Unable to update without version number argument");
                    }
                });
        }
    }
}
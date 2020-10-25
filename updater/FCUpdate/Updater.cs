using System;
using System.Collections.Generic;
using System.Net;
using System.IO;
using System.Diagnostics;
using System.Runtime.InteropServices;
using CommandLine;


namespace FCUpdate
{
    class Updater
    {
        public class Options
        {
            [Option('v', "version", Required = true, HelpText = "Update FinalCif to this version.")]
            public string Version { get; set; }
        }

        private static string GetDownloadUrl()
        {
            var downloadUrl = "unknown system";
            if (IsWindows())
            {
                downloadUrl = "https://xs3-data.uni-freiburg.de/finalcif/FinalCif-setup-x64-v{0}.exe";
            }
            if (IsOSX())
            {
                downloadUrl = "https://xs3-data.uni-freiburg.de/finalcif/Finalcif-v{0}_macos.app.zip";
            }
            if (IsLinux())
            {
                downloadUrl = "https://xs3-data.uni-freiburg.de/finalcif/FinalCif-v{}_ubuntu";
            }
            return downloadUrl;
        }

        private string GetSetupName()
        {
            string setup_name = "no_setup_name";
            if (IsWindows())
            {
                setup_name = "FinalCif-setup-x64-v{0}.exe";
            }
            Console.WriteLine(RuntimeInformation.OSDescription, RuntimeInformation.OSArchitecture);
            if (IsOSX())
            {
                setup_name = "Finalcif-v{0}_macos.app.zip";
            }
            if (IsLinux())
            {
                setup_name = "FinalCif-v{}_ubuntu";
            }
            return setup_name;
        }

        private static bool IsOSX()
        {
            return RuntimeInformation.IsOSPlatform(OSPlatform.OSX);
        }

        private static bool IsLinux()
        {
            return RuntimeInformation.IsOSPlatform(OSPlatform.Linux);
        }
        
        private static bool IsWindows()
        {
            return RuntimeInformation.IsOSPlatform(OSPlatform.Windows);
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
            catch (Exception)
            {
                Console.WriteLine("Unable to run updater");
                return 0;
            }

            return 0;
        }

        private static void KillProcesses(IEnumerable<Process> processList)
            /* Kills all FinalCif processes */
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

        private string MoveTempToExeFile(string version, string tempFile)
        {
            string targetDir = Directory.GetCurrentDirectory();
            string exeFile = Path.Combine(targetDir, string.Format(GetSetupName(), version));
            Console.WriteLine("Move to exe file: {0}", exeFile);
            File.Move(tempFile, exeFile, true);
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
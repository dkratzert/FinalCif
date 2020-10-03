using System;
using System.Diagnostics;
using System.ComponentModel;

namespace FCUpdate
{

    class ProcessList
    {
        public void FindRunningFinalCif()
        {
            Console.WriteLine("FinalCif Updater");
            Console.WriteLine("Fetching update from server...");

            Process[] processList = Process.GetProcessesByName("FinalCif");
            foreach (var process in processList)
            {
                Console.WriteLine("Process: " + process);
                Console.WriteLine("Ending process {0}", process.ToString());
                process.Kill();
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
           ProcessList p = new ProcessList();
            p.FindRunningFinalCif();
        }
    }
}



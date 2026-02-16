/*
 * Please note in order to update the modal need to use the ConnectReference instead of WebReference, and for using the Connected Reference, need to install ODataConnectedService Extensions
 * if you have problem, please refer to registry setting by using this link https://github.com/OData/lab/issues/64
 */

using System;
using System.Collections.Generic;
using System.Configuration;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Net.Mail;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Web.Administration;
using System.Net;
using System.Threading;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using CdaExtractor.ProviderPortalODataService;
using System.Web;

namespace CdaExtractor
{
    class Program
    {
        #region Exception Handling

        /// <summary>
        /// Logs to the event log as a backup to log4net
        /// </summary>
        /// <param name="message">The message to log</param>
        /// <param name="source">The source string to use</param>
        /// <param name="type">The type of event</param>
        /// <param name="eventID">The id of the event</param>
        public static void WriteToEventLog(string message, string source = "Cyfluent", EventLogEntryType type = EventLogEntryType.Error, int eventID = 0, string facilityCode = null)
        {
            try
            {
                message = (message ?? string.Empty);
                const string sLog = "Application";
                if (!EventLog.SourceExists(source))
                {
                    EventLog.CreateEventSource(source, sLog);
                }
                var subs = message.Substring(0, Math.Min(message.Length, 10000));
                EventLog.WriteEntry(source, subs, type, eventID);
            }
            catch(Exception e)
            {
                //squelch
            }
        }

        static void UnhandledExceptionTrapper(object sender, UnhandledExceptionEventArgs e)
        {
            var msg = "Cda extract execution halted due to the following error(s): " + Environment.NewLine + e.ExceptionObject.ToString();
            WriteToEventLog(msg);
            Console.WriteLine(msg);
            Console.WriteLine("Press Enter to continue");
            Console.ReadLine();
            Environment.Exit(1);
        }

        private static void timerC(object state)
        {
            Environment.Exit(0);
        }
        #endregion

        #region settings
        private static DateTime StartDate = Convert.ToDateTime(ConfigurationManager.AppSettings["startDate"]);
        private static DateTime EndDate = Convert.ToDateTime(ConfigurationManager.AppSettings["endDate"]);
        private static bool Debugging
        {
            get
            {
                var debug = false;
#if DEBUG
                debug = true;
#else
            
#endif
                return debug;
            }
        }
        private static FileType ExtractFileType
        {
            get
            {
                var extractFileType = (ConfigurationManager.AppSettings["extractFileType"] ?? string.Empty).Trim().ToLower();
                if (extractFileType.Contains("hl7")) return FileType.Hl7;
                return FileType.Cda;
            }
        }

        enum FileType
        {
            Cda,
            Hl7
        }
        #endregion settings

        static void Main(string[] args)
        {
            #region scrub/exceptions
            AppDomain.CurrentDomain.UnhandledException += UnhandledExceptionTrapper;
            TimeSpan endOfBusinessHours = new TimeSpan(17, 0, 0); //5pm
            TimeSpan startOfBusinessHours = new TimeSpan(7, 0, 0); //7am
            TimeSpan now = DateTime.Now.TimeOfDay;

            if ((now > startOfBusinessHours) && (now < endOfBusinessHours))
            {
                //throw new Exception("You cannot run this utility between 7am and 5pm");
            }
            if (ExtractFileType != FileType.Cda) throw new NotSupportedException("only cda extract type is supported at this time");
            #endregion

            DateTime dateStart;
            DateTime dateEnd;
            Console.WriteLine("Enter the Start Date (MM/DD/YYYY):  ");
            var startDate = Console.ReadLine();

            try
            {
                dateStart = DateTime.Parse(startDate);
            }
            catch (Exception ex)
            {
                throw ex;
            }

            Console.WriteLine("Enter the End   Date (MM/DD/YYYY):  ");
            var endDate = Console.ReadLine();
            if (string.IsNullOrEmpty(endDate))
            {
                dateEnd = dateStart.AddDays(1);
            }
            else
            {
                try
                {
                    dateEnd = DateTime.Parse(endDate);
                }
                catch (Exception ex)
                {
                    throw ex;
                }
            }

            //Console.WriteLine("Enter the Start Date (MM/DD/YYYY):  ");
            //var startDate = string.Empty;
            //while (true)
            //{
            //    ConsoleKeyInfo k = Console.ReadKey();
            //    if (k.Key == ConsoleKey.Enter) break;
            //    //Console.Write(k);
            //}

            #region set up the provider
            var c = new Provider
            {
                HumanResourceID = "5f185a7b-a22a-4871-8f22-ba48f19b2686",
                FirstName = "Doctor",
                LastName = "Physician",
                Title = "MD",
                Username = "xxx",
                Password = "xxxxxxxxxx",
                FacilityID = "d47fb03a-0571-4ede-bae2-b15bce8afa3c",
                FacilityCode = "PCare",
                LoginUrl = @"https://beta.cyfluentchart.com/ProviderPortal/ONCBeta/Default.aspx"
            };
            c.LogIn();
            #endregion

            #region pull the patient data and start the extracts
            Console.WriteLine();
            Console.WriteLine("Pulling patient data...");
            //c.ctx.CodeDiets.Expand("CodeSetDiet").Take(50).Select(d => new { d.Code, d.CodeDescription, d.CodeDietID, d.CodeSetDietID, d.LogicalOrder, d.ObjectVersionDate }).ToList();
            var query = c.ctx.Patients.Where(pat => pat.Encounters.Any(e => e.EncounterStartDateTime >= dateStart && e.EncounterStartDateTime <= dateEnd && !e.Converted));
            var pats = query.OrderBy(p => p.ObjectVersionDate).Take(30)
                .Select(pat => new { pat.PatientID, pat.FirstName, pat.LastName, pat.AccountNumber, pat.BirthDate, pat.Gender.GenderName, pat.PrimaryLanguageName, pat.SecondaryLanguageName, pat.AssignedPhysicianID, pat.ReferringProviderID }).ToList().Distinct().ToList();
            Console.WriteLine("Downloading extracts...");
            var patientCount = pats.Count;
            for (int i = 0; i < patientCount; i++)
            {
                var pat = pats[i];
                if (pat == null || string.IsNullOrWhiteSpace(pat.PatientID)) continue;

                Console.WriteLine("Pulling extract for " + pat.FirstName + " " + pat.LastName + " (" + (i + 1) + @"/" + patientCount + ")");
                try
                {
                    /*
Patient Name
Sex
Date of Birth
Race
Ethnicity
Preferred Language
Smoking Status
Problems
Medications
Medication Allergies
Laboratory Tests
Laboratory Values(s)/Result(s)
Vital Signs
Procedures
Care Team Member(s)
Immunizations
Unique Device Identifier(s) for a Patient’s Implantable Device(s)
Assessment and Plan of Treatment
Goals
Health Concerns

                     */
                    var xml = c.GetCda(pat.PatientID);
                    var doc = System.Xml.Linq.XDocument.Parse(xml);
                    var fn = (pat.PatientID + "_" + pat.FirstName + "_" + pat.LastName + "_" + (pat.AccountNumber ?? string.Empty) + "_Extract");
                    if (!Directory.Exists(@"C:\Temp")) Directory.CreateDirectory(@"C:\Temp");
                    var filePath = Path.Combine(@"C:\Temp", fn + ".xml");
                    File.WriteAllText(filePath, xml);
                    var allergies = c.ctx.PatientAllergies.Where(a => a.PatientID == pat.PatientID && a.ObjectVersionDate >= StartDate && a.ObjectVersionDate <= EndDate).ToList();
                    var problems = c.ctx.PatientProblems.Where(a => a.PatientID == pat.PatientID
                        && a.OnsetDate != null && a.OnsetDate >= new DateTime(2005, 1, 1) && a.OnsetDate <= new DateTime(2007, 12, 31)
                    ).ToList();
                    var race = c.ctx.PatientRaces.Where(a => a.PatientID == pat.PatientID).ToList();
                    var preferredLanguage = new { pat.PrimaryLanguageName };
                    var r = race.Select(ra => ra.FacilityRaceID).ToArray();
                    var race2 = race.Any() ? c.ctx.FacilityRaces.Where(fr => r[0] == fr.FacilityRaceID).ToList() : null;
                    var ethnicity = c.ctx.PatientEthnicities.Where(a => a.PatientID == pat.PatientID).ToList();
                    var e = ethnicity.Select(ra => ra.FacilityEthnicityID).ToArray();
                    var eth2 = ethnicity.Any() ? c.ctx.FacilityEthnicities.Where(fr => e[0] == fr.FacilityEthnicityID).ToList() : null;
                    var soc = c.ctx.PatientSocialHistories.Where(a => a.PatientID == pat.PatientID).Select(s => new
                    {
                        s = s,
                        stat = s.SmokingStatu
                    }).ToList();
                    var meds = c.ctx.PatientPrescriptions.Where(a => a.PatientID == pat.PatientID).ToList();
                    var orders = c.ctx.ActionItems.Where(a => a.PatientID == pat.PatientID).Select(ai => new {
                        ai.PatientID,
                        ai.ActionableItemCode,
                        ai.ActionableItemDescription
                    }).ToList();
                    var planAndInstructions = c.ctx.ActionItems.Where(a => a.PatientID == pat.PatientID && a.ActionItemType.ActionItemTypeName.StartsWith("Plan")).ToList();
                    var res = c.ctx.ActionItemResults.Where(a => a.ActionItem.PatientID == pat.PatientID).ToList();
                    var resValues = c.ctx.ActionItemResultValues.Where(a => a.ActionItemResult.ActionItem.PatientID == pat.PatientID).ToList();
                    var adminMed = c.ctx.ActionItemResultAdminMedications.Where(a => a.ActionItemResult.ActionItem.PatientID == pat.PatientID).ToList();
                    var vitals = c.ctx.PatientVitals.Where(a => a.PatientID == pat.PatientID).ToList();
                    var enc = c.ctx.Encounters.Where(a => a.PatientID == pat.PatientID).ToList();

                    var devices = c.ctx.PatientImplantableDevices.Where(d => d.PatientID == pat.PatientID).ToList();
                    var encounters = c.ctx.Encounters.Where(d => d.Patient.PatientID == pat.PatientID).ToList();
                    List<CareTeamMember> careTeamMembers = new List<CareTeamMember>();
                    var careteam = c.ctx.HumanResources.Where(h => h.HumanResourceID == pat.AssignedPhysicianID).Select(hr => new { hr.FirstName, hr.LastName, hr.Title }).ToList();
                    var careteam1 = c.ctx.FacilityAssociates.Where(fa => fa.FacilityAssociateID == pat.ReferringProviderID).Select(fa => new { fa.AssociateFirstName, fa.AssociateLastName, fa.FacilityAssociateType.FacilityAssociateTypeName }).ToList();
                    var careteam2 = c.ctx.EncounterAssociatedProviders.Where(p => p.Encounter.PatientID == pat.PatientID).Select(eap => new { eap.HumanResource.FirstName , eap.HumanResource.LastName, eap.HumanResource.Title }).ToList();
                    if (careteam.Any()) careTeamMembers.Add(new CareTeamMember { FirstName = careteam.FirstOrDefault().FirstName, LastName = careteam.FirstOrDefault().LastName, Title = careteam.FirstOrDefault().Title });
                    if (careteam1.Any()) careTeamMembers.Add(new CareTeamMember { FirstName = careteam1.FirstOrDefault().AssociateFirstName, LastName = careteam1.FirstOrDefault().AssociateLastName, Title = careteam1.FirstOrDefault().FacilityAssociateTypeName.StartsWith("Providers") ? "Dr.": string.Empty });
                    if (careteam2.Any()) careTeamMembers.Add(new CareTeamMember { FirstName = careteam2.FirstOrDefault().FirstName, LastName = careteam2.FirstOrDefault().LastName, Title = careteam2.FirstOrDefault().Title });

                    var careplans = c.ctx.PatientCarePlans.Where(a => a.PatientID == pat.PatientID).ToList();
                    var observations = c.ctx.PatientCarePlanObservations.Where(a => a.PatientCarePlan.PatientID == pat.PatientID).ToList();
                    var interventions = c.ctx.PatientCarePlanInterventions.Where(a => a.PatientCarePlan.PatientID == pat.PatientID).ToList();
                    var healthconcerns = c.ctx.PatientCarePlanHealthConcerns.Where(a => a.PatientCarePlan.PatientID == pat.PatientID).ToList();
                    var goals = c.ctx.PatientCarePlanGoals.Where(a => a.PatientCarePlan.PatientID == pat.PatientID).ToList();
                    var evalandoutcomes = c.ctx.PatientCarePlanEvaluationAndOutComes.Where(a => a.PatientCarePlan.PatientID == pat.PatientID).ToList();

                    var bl = false;
                }
                catch (Exception e)
                {
                }
            }
            #endregion
            Console.WriteLine("Finished downloading extracts ...");
            Console.ReadLine();
        }
        
        class CareTeamMember
        {
            public string FirstName { get; set; }
            public string LastName { get; set; }
            public string Title { get; set; }
        }

        #region get urls with user login info
        private static bool UrlIsValid(string url)
        {
            try
            {
                HttpWebRequest request = HttpWebRequest.Create(url) as HttpWebRequest;
                request.Timeout = 2000; //set the timeout to 2 seconds to keep the user from waiting too long for the page to load
                request.Method = "HEAD"; //Get only the header information -- no need to download any content

                using (HttpWebResponse response = request.GetResponse() as HttpWebResponse)
                {
                    int statusCode = (int)response.StatusCode;
                    if (statusCode >= 100 && statusCode < 400) //Good requests
                    {
                        return true;
                    }
                    else if (statusCode >= 500 && statusCode <= 510) //Server Errors
                    {
                        //log.Warn(String.Format("The remote server has thrown an internal error. Url is not valid: {0}", url));
                        return false;
                    }
                }
            }
            catch (WebException ex)
            {
                if (ex.Status == WebExceptionStatus.ProtocolError) //400 errors
                {
                    return false;
                }
                else
                {
                    //log.Warn(String.Format("Unhandled status [{0}] returned for url: {1}", ex.Status, url), ex);
                }
            }
            catch (Exception ex)
            {
                //log.Error(String.Format("Could not test url {0}.", url), ex);
            }
            return false;
        }

        private static async Task<object> CallPostHandler(string url)
        {
            byte[] result;
            byte[] buffer = new byte[4096];
            try
            {
                HttpWebRequest request = HttpWebRequest.Create(url) as HttpWebRequest;
                request.Timeout = 120000;
                request.Method = "GET";

                var tsk = request.GetResponseAsync();
                var response = (HttpWebResponse)await tsk;//request.GetResponse() as HttpWebResponse;

                int statusCode = (int)response.StatusCode;
                if (statusCode >= 100 && statusCode < 400) //Good requests
                {
                    if ((url ?? string.Empty).ToLower().Contains("getreportpdf"))
                    {
                        using (Stream responseStream = response.GetResponseStream())
                        {
                            using (MemoryStream memoryStream = new MemoryStream())
                            {
                                int count = 0;
                                do
                                {
                                    count = responseStream.Read(buffer, 0, buffer.Length);
                                    memoryStream.Write(buffer, 0, count);

                                } while (count != 0);

                                result = memoryStream.ToArray();
                                return result;
                            }
                        }
                    }
                    using (StreamReader reader = new StreamReader(response.GetResponseStream()))
                    {
                        string xmlString = (reader.ReadToEnd() ?? string.Empty).Trim();
                        if (string.IsNullOrWhiteSpace(xmlString)) return xmlString; //+1 for unit tests :)
                        if (!xmlString.StartsWith("<") && !xmlString.EndsWith(">")) return xmlString;
                        if (xmlString.ToLower().Contains("Invalid login".ToLower())) return null;

                        try
                        {
                            var xml = System.Xml.Linq.XDocument.Parse(string.Format("<Root>{0}</Root>", xmlString));
                            return xml;
                        }
                        catch (Exception e)
                        {
                            var msg = e.Message + "\n\nStack Trace:\n" + e.StackTrace;
                            //Config.WriteLine(msg);
                            return xmlString;
                        }
                    }
                }
                else if (statusCode >= 500 && statusCode <= 510) //Server Errors
                {
                    //log.Warn(String.Format("The remote server has thrown an internal error. Url is not valid: {0}", url));
                    return null;
                }
            }
            catch (WebException ex)
            {
                var msg = ex.Message + "\n\nStack Trace:\n" + ex.StackTrace;
                //Config.WriteLine(msg);
                if (ex.Status == WebExceptionStatus.ProtocolError) //400 errors
                {
                    return null;
                }
                else
                {
                    //log.Warn(String.Format("Unhandled status [{0}] returned for url: {1}", ex.Status, url), ex);
                }
            }
            catch (Exception ex)
            {
                var msg = ex.Message + "\n\nStack Trace:\n" + ex.StackTrace;
                //Config.WriteLine(msg);
                //log.Error(String.Format("Could not test url {0}.", url), ex);
            }
            return null;
        }
        #endregion
    }

    public class Provider
    {
        public class LoginRequestObj
        {
            public string userKey;
            public string cookiestr;
        }

        private string userKey;
        private string cookiestr;
        private CookieContainer container;

        public string HumanResourceID;
        public string FirstName;
        public string LastName;
        public string Title;
        public string Username;
        public string Password;
        public string FacilityID;
        public string FacilityCode;
        public string LoginUrl;
        public string Xml;
        
        public void Logout()
        {
            userKey = null;
            cookiestr = null;
        }

        public Entities ctxOld
        {
            get
            {
                var vl = new Entities(new Uri(LoginUrl.Replace("Default.aspx", "Secure/oData.svc")));
                vl.SendingRequest2 += AddAuthHeader;
                vl.Timeout = 180;
                return vl;
            }
        }

        public CfChartOpModel.Entities ctx
        {
            get
            {
                var vl = new CfChartOpModel.Entities(new Uri(LoginUrl.Replace("Default.aspx", "Secure/oData.svc")));
                vl.SendingRequest2 += AddAuthHeader;
                vl.Timeout = 180;
                return vl;
            }
        }

        private void AddAuthHeader(object sender,
            System.Data.Services.Client.SendingRequest2EventArgs e)
        {
            e.RequestMessage.SetHeader("Authorization", GetAuthHeader(e.RequestMessage.Url.ToString()));
            e.RequestMessage.SetHeader("Cookie", container.GetCookieHeader(e.RequestMessage.Url));
        }

        public void LogIn()
        {
            if (!string.IsNullOrWhiteSpace(userKey) && !string.IsNullOrWhiteSpace(cookiestr)) return;
            var url = LoginUrl + "/GetUserKeyAndCookieString";
            var payload = JsonConvert.SerializeObject(new JObject
            {
                new JProperty("userName", Username),
                new JProperty("password", Password),
                new JProperty("facilityCode", FacilityCode),
                new JProperty("facilityID", FacilityID),
                new JProperty("hrId", HumanResourceID)
            });
            ASCIIEncoding encoder = new ASCIIEncoding();
            byte[] data = encoder.GetBytes(payload);
            HttpWebRequest request = HttpWebRequest.Create(url) as HttpWebRequest;
            request.Timeout = 120000;
            request.Method = "POST";
            request.ContentLength = data.Length;
            request.ContentType = "application/json";
            request.Expect = "application/json";

            request.GetRequestStream().Write(data, 0, data.Length);

            using (var response = request.GetResponse() as HttpWebResponse)
            using (StreamReader reader = new StreamReader(response.GetResponseStream()))
            {
                string str = (reader.ReadToEnd() ?? string.Empty).Trim();
                var obj = JsonConvert.DeserializeObject<LoginRequestObj>((((Newtonsoft.Json.Linq.JValue)(JObject.Parse(str)["d"])).Value).ToString());
                userKey = obj.userKey;
                cookiestr = obj.cookiestr;
                
                var ck = new Cookie(System.Web.Security.FormsAuthentication.FormsCookieName, cookiestr)
                {
                    Path = System.Web.Security.FormsAuthentication.FormsCookiePath,
                    Secure = System.Web.Security.FormsAuthentication.RequireSSL,
                    Expires = DateTime.MaxValue,
                    Domain = new Uri(url).Host
                };
                var con = new CookieContainer();
                con.Add(ck);
                container = con;
            }
        }

        public string GetCda(string patientID, DateTime? start = null, DateTime? end = null)
        {
            start = start ?? DateTime.UtcNow.AddYears(-130);
            end = end ?? DateTime.UtcNow.AddYears(130);
            LogIn();
            var url = LoginUrl.Replace("Default.aspx", "Secure/Home/File.ashx?mode=dataccd&id=" + patientID + "&f=" + FacilityID + "&u=" + Username + "&isProv=true&start=" + HttpUtility.UrlEncode(start.Value.ToString()) + "&end=" + HttpUtility.UrlEncode(end.Value.ToString()));
            HttpWebRequest request = HttpWebRequest.Create(url) as HttpWebRequest;
            request.Timeout = 120000;
            request.Method = "GET";
            request.ContentType = "application/xml";
            request.Expect = "application/xml";
            request.CookieContainer = container;
            request.AllowAutoRedirect = false;
            request.Headers["Authorization"] = GetAuthHeader(url);

            using (var response = request.GetResponse() as HttpWebResponse)
            using (StreamReader reader = new StreamReader(response.GetResponseStream()))
            {
                string str = (reader.ReadToEnd() ?? string.Empty).Trim();
                var xml = System.Xml.Linq.XDocument.Parse(str); // string.Format("<Root>{0}</Root>", str));
                return str;
            }
        }

        private string GetAuthHeader(string url)
        {
            var rgx = new System.Text.RegularExpressions.Regex(@"/\s/g");
            var encodedUrl = rgx.Replace(url, "+");
            var cleanedUrl = (encodedUrl.IndexOf("?") > -1) ? encodedUrl.Substring(0, encodedUrl.IndexOf("?")) : encodedUrl;
            cleanedUrl = cleanedUrl.Replace("../", string.Empty);
            cleanedUrl = (cleanedUrl.IndexOf("Secure/") > -1) ? cleanedUrl.Substring(cleanedUrl.IndexOf("Secure/")) : cleanedUrl;

            // hash the URL for HMAC
            var hasher = new System.Security.Cryptography.HMACSHA256(System.Text.Encoding.ASCII.GetBytes(userKey));
            var hmac = hasher.ComputeHash(System.Text.Encoding.ASCII.GetBytes(cleanedUrl));
            string hex = BitConverter.ToString(hmac);
            hex = hex.Replace("-", "");
            var headerString = Username + ":" + FacilityID + ":" + hex;
            return headerString;
        }
    }
}

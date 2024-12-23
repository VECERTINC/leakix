import requests
import json
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def read_api_key():
    with open('api_key.txt', 'r') as file:
        return file.read().strip()

def save_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def consultar_ip(ip, api_key):
    url = f"https://leakix.net/host/{ip}"
    headers = {
        'api-key': api_key,
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def consultar_dominio(domain, api_key):
    url = f"https://leakix.net/domain/{domain}"
    headers = {
        'api-key': api_key,
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def buscar_subdominios(domain, api_key):
    url = f"https://leakix.net/api/subdomains/{domain}"
    headers = {
        'api-key': api_key,
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def consulta_general(query, api_key):
    url = f"https://leakix.net/search?scope=&page=0&q={query}"
    headers = {
        'api-key': api_key,
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print(Fore.RED + "Error: Unable to decode JSON response.")
            return {}
    else:
        print(Fore.RED + f"Error: Received response with status code {response.status_code}.")
        return {}

def mostrar_biblioteca_dorks():
    dorks = [
        ("Search in France", '+(country:"France" host:"fr")'),
        ("Results in Europe without Russia", '+geoip.continent_name:"Europe" -country:"Russia"'),
        ("Filter by severity (GitConfigHttpPlugin critical)", '(+plugin:"GitConfigHttpPlugin" +severity:"critical") (+plugin:"DotDsStoreOpenPlugin" +severity:"high")'),
        ("Filter dataset larger than 1GB with ransom note", '+dataset.infected:true +dataset.size:>10000000000'),
        ("Filter ransom note containing btc", '+dataset.ransom_notes:"btc"'),
        ("Results with FortiGate as SSL issuer", '+ssl.certificate.issuer_name:"FortiGate"'),
        ("Results with .co.uk in SSL Common Names or domains", 'ssl.certificate.cn:"co.uk" ssl.certificate.domain:"co.uk"'),
        ("Results with .co.uk created after 2023-01-01", '+(ssl.certificate.cn:"co.uk" ssl.certificate.domain:"co.uk") +creation_date:>2023-01-01')
    ]

    print(Fore.CYAN + "\nDork Library:")
    for description, query in dorks:
        print(f"{Fore.YELLOW}{description}: {Fore.WHITE}{query}")

def mostrar_plugins():
    plugins = [
        ("ApacheActiveMQ", "Apache ActiveMQ is outdated", "Trusted/Pro members only"),
        ("ApacheOFBizPlugin", "Apache OFBiz is outdated", "Trusted/Pro members only"),
        ("ApacheStatusPlugin", "Apache server-status page is publicly available", "Public"),
        ("BitbucketPlugin", "BitBucket instance outdated", "Trusted/Pro members only"),
        ("CentosWebPanelPlugin", "CentOS Web Panel outdated", "Public"),
        ("CheckMkPlugin", "CheckMK monitoring endpoint publicly available", "Public"),
        ("CheckpointGwPlugin", "Check Point Gateway is outdated", "Trusted/Pro members only"),
        ("CiscoRV", "Cisco RV hardware outdated", "Public"),
        ("CitrixADCPlugin", "Citrix ADC appliance is outdated", "Trusted/Pro members only"),
        ("CloudPanelPlugin", "CloudPanel is outdated", "Public"),
        ("ConfigJsonHttp", "A JSON configuration file has been found", "Public"),
        ("ConfluenceVersionIssue", "Confluence instance outdated", "Trusted/Pro members only"),
        ("ConnectWiseScreenConnect", "ConnectWise ScreenConnect is vulnerable", "Public"),
        ("Consul", "Consul server is public", "Public"),
        ("CouchDbOpenPlugin", "CouchDB instance is public", "Public"),
        ("CrushFTPPlugin", "CrushFTP service outdated", "Trusted/Pro members only"),
        ("CyberPanelPlugin", "CyberPanel is outdated", "Trusted/Pro members only"),
        ("DeadMon", "NAS has been infected by DeadBolt", "Public"),
        ("DockerRegistryHttpPlugin", "Docker registry is public", "Public"),
        ("DotDsStoreOpenPlugin", "MacOS file listing through .DS_Store file", "Public"),
        ("DotEnvConfigPlugin", "Dotenv file configuration is publicly accessible", "Trusted/Pro members only"),
        ("ElasticSearchOpenPlugin", "ElasticSearch is publicly available", "Public"),
        ("EsxVersionPlugin", "ESXi hypervisor outdated", "Trusted/Pro members only"),
        ("ExchangeVersion", "Microsoft Exchange Server is outdated", "Trusted/Pro members only"),
        ("FortiGatePlugin", "FortiGate instance outdated", "Trusted/Pro members only"),
        ("FortiOSPlugin", "FortiGate instance outdated", "Trusted/Pro members only"),
        ("GenericDvrPlugin", "Vulnerable Generic DVR", "Public"),
        ("GitConfigHttpPlugin", "Git configuration and history exposed", "Public"),
        ("GitlabPlugin", "Gitlab instance looks outdated", "Public"),
        ("GoAnywhereMFT", "Exposed GoAnywhere MFT administration interface", "Public"),
        ("GrafanaOpenPlugin", "Grafana instance publicly available", "Public"),
        ("HiSiliconDVR", "Vulnerable HiSilicon family DVR", "Public"),
        ("HttpNTLM", "Server accepting anonymous credentials", "Public"),
        ("IOSEXPlugin", "Cisco IOS EX implant detected", "Trusted/Pro members only"),
        ("IvantiConnectSecure", "Ivanti Connect Secure outdated", "Trusted/Pro members only"),
        ("JenkinsOpenPlugin", "Jenkins is publicly available", "Public"),
        ("JenkinsVersionPlugin", "Jenkins service outdated", "Trusted/Pro members only"),
        ("JiraPlugin", "Jira instance outdated", "Trusted/Pro members only"),
        ("JunosJWebPlugin", "Juniper device is outdated", "Trusted/Pro members only"),
        ("KafkaOpenPlugin", "Kafka instance is public", "Public"),
        ("LaravelTelescopeHttpPlugin", "Laravel development panel enabled", "Public"),
        ("Log4JOpportunistic", "Server vulnerable to Log4J CVE-2021-44228", "Public"),
        ("MetabaseHttpPlugin", "Metabase is outdated", "Trusted/Pro members only"),
        ("MinioPlugin", "MinIO instance is outdated", "Trusted/Pro members only"),
        ("MirthPlugin", "Mirth Connect is out-dated", "Trusted/Pro members only"),
        ("MobileIronCorePlugin", "Ivanti MobileIron core is outdated", "Trusted/Pro members only"),
        ("MobileIronSentryPlugin", "Ivanti MobileIron Sentry is outdated", "Trusted/Pro members only"),
        ("MongoOpenPlugin", "MongoDB is publicly available", "Public"),
        ("MoodlePlugin", "Moodle is vulnerable", "Public"),
        ("MysqlOpenPlugin", "MySQL is publicly available", "Public"),
        ("NexusRepoPlugin", "Nexus Repository is outdated", "Trusted/Pro members only"),
        ("OpenEdgePlugin", "OpenEdge is outdated", "Trusted/Pro members only"),
        ("PaloAltoPlugin", "Palo Alto firewall outdated", "Trusted/Pro members only"),
        ("PaperCutPlugin", "PaperCut is outdated", "Trusted/Pro members only"),
        ("PhpCgiRcePlugin", "CGI executing PHP code", "Trusted/Pro members only"),
        ("PhpInfoHttpPlugin", "Found php information file", "Public"),
        ("PhpStdinPlugin", "Application executing PHP code", "Trusted/Pro members only"),
        ("ProxyOpenPlugin", "Server accepting proxy connections", "Trusted/Pro members only"),
        ("PulseConnectPlugin", "Pulse Connect Secure outdated", "Trusted/Pro members only"),
        ("QnapVersion", "QNAP NAS outdated", "Trusted/Pro members only"),
        ("RedisOpenPlugin", "Redis instance is public", "Public"),
        ("SharePointPlugin", "Microsoft SharePoint Server is outdated", "Trusted/Pro members only"),
        ("SmbPlugin", "Open SMB file sharing detected", "Public"),
        ("SolrOpenPlugin", "Solr administration is publicly available", "Public"),
        ("SolrVersionPlugin", "Solr instance is outdated", "Trusted/Pro members only"),
        ("SonarQubePlugin", "SonarQube instance is public", "Public"),
        ("SonicWallGMSPlugin", "SonicWall GMS outdated", "Trusted/Pro members only"),
        ("SonicWallSMAPlugin", "SonicWall firewall outdated", "Trusted/Pro members only"),
        ("SophosPlugin", "Sophos firewall outdated", "Public"),
        ("SplunkPlugin", "Splunk Enterprise outdated", "Trusted/Pro members only"),
        ("SshRegresshionPlugin", "SSH is potentially vulnerable", "Public"),
        ("SymfonyProfilerPlugin", "Symfony development panel enabled", "Public"),
        ("SymfonyVerbosePlugin", "Symfony error leaking informations", "Public"),
        ("SysAidPlugin", "SysAid instance outdated", "Trusted/Pro members only"),
        ("TeamCityPlugin", "TeamCity Server is outdated", "Trusted/Pro members only"),
        ("TraversalHttpPlugin", "Detected HTTP traversal vulnerability", "Public"),
        ("VCenterVersionPlugin", "VMWare vSphere/vCenter outdated", "Trusted/Pro members only"),
        ("veeaml9", "Veeam distribution service outdated", "Trusted/Pro members only"),
        ("VeeamPlugin", "Veeam Backup & Recovery outdated", "Trusted/Pro members only"),
        ("ViciboxPlugin", "Vicidial Recordings exposure", "Trusted/Pro members only"),
        ("VinChinBackupPlugin", "VinChin VMWare Backup exposed and vulnerable", "Trusted/Pro members only"),
        ("VMWareCloudDirector", "VMWare Cloud Director exposed and vulnerable", "Public"),
        ("VsCodeSFTPPlugin", "VSCode SFTP configuration exposed", "Public"),
        ("WpUserEnumHttp", "Wordpress user enumeration", "Trusted/Pro members only"),
        ("WsFTPPlugin", "WS_FTP service is outdated", "Trusted/Pro members only"),
        ("Wso2Plugin", "WSO2 product looks outdated", "Public"),
        ("YiiDebugPlugin", "Yii development panel enabled", "Trusted/Pro members only"),
        ("ZimbraPlugin", "Zimbra server is outdated", "Trusted/Pro members only"),
        ("ZookeeperOpenPlugin", "Zookeeper server is public", "Public"),
        ("ZyxelVersion", "Zyxel firewall outdated", "Trusted/Pro members only"),
    ]

    print(Fore.CYAN + "\nPlugins List:")
    for plugin, description, access in plugins:
        print(f"{Fore.YELLOW}{plugin}: {Fore.WHITE}{description} ({Fore.GREEN}Access: {access})")

def mostrar_respuesta_consulta_general(result):
    print(Fore.MAGENTA + "\nQuery Result:")
    formatted_result = json.dumps(result, indent=4)
    print(formatted_result)
    return formatted_result

def main():
    print(Fore.GREEN + r"""
       .--.       .--.
    _  `    \     /    `  _
     `\.===. \.^./ .===./`
            \/`"`\/
         , |VECERT |  ,
        / `\|;-.-'|/` \
       /    |::\  |    \
    .-' ,-'`|:::; |`'-, '-.
        |   |::::\|   | 
        |   |::::;|   |
        |   \:::://   |
        |    `.://'   | Leakix CLI
       .'             `. Create an account at: leakix.net
    _,'                 `,_
    """)
    api_key = read_api_key()
    
    while True:
        print(Fore.CYAN + "\nMenu:")
        print(f"1 - Query IP address 🌐  |  2 - Query domain 🌍  |  3 - Search subdomains 🔍")
        print(f"4 - General query in Leakix 📊  |  5 - Dork Library 📚  |  6 - Plugins 🛠️")
        print("0 - Exit ❌")
        
        choice = input("Select an option: ")

        if choice == '1':
            ip = input("Enter the IP address: ")
            result = consultar_ip(ip, api_key)
            formatted_result = mostrar_respuesta_consulta_general(result)
            save_to_file("query_ip_result.txt", formatted_result)

        elif choice == '2':
            domain = input("Enter the domain: ")
            result = consultar_dominio(domain, api_key)
            formatted_result = mostrar_respuesta_consulta_general(result)
            save_to_file("query_domain_result.txt", formatted_result)

        elif choice == '3':
            domain = input("Enter the domain to search for subdomains: ")
            result = buscar_subdominios(domain, api_key)
            formatted_result = mostrar_respuesta_consulta_general(result)
            save_to_file("query_subdomains_result.txt", formatted_result)

        elif choice == '4':
            query = input("Enter the general query: ")
            result = consulta_general(query, api_key)
            formatted_result = mostrar_respuesta_consulta_general(result)
            save_to_file("query_general_result.txt", formatted_result)

        elif choice == '5':
            mostrar_biblioteca_dorks()  # Show the dork library

        elif choice == '6':
            mostrar_plugins()  # Show the plugins library

        elif choice == '0':
            print(Fore.RED + "Exiting...")
            break

        else:
            print(Fore.RED + "Invalid option. Please try again.")

if __name__ == "__main__":
    main()

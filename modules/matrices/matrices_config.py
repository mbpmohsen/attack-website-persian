from string import Template

module_name = "Matrices"
priority = 2

# Matrix markdown path
matrix_markdown_path = "content/pages/matrices/"

# Path for templates
matrices_templates_path = "modules/matrices/templates/"

# Matrix overview string
matrix_overview_md = (
    "Title: Matrix Overview \n"
    "Template: general/redirect-index \n"
    "RedirectLink: /matrices/enterprise/ \n"
    "private: True \n"
    "save_as: matrices/index.html"
)

# String template for main domain matrices
matrix_md = Template(
    "Title: Matrix-${domain}\n"
    "Slug: ${slug}\n"
    "url: /matrices/${path}/\n"
    "Template: matrices/matrix\n"
    "save_as: matrices/${path}/index.html\n"
    "data: "
)

# String template for platform matrices
platform_md = Template(
    "Title: Matrix-${domain}-${platform}\n"
    "Template: matrices/matrix\n"
    "save_as: matrices/${domain}/${platform_path}/index.html\n"
    "data: "
)

sidebar_matrices_md = (
    "Title: Matrices Sidebar\n"
    "Template: general/sidebar-template \n"
    "save_as: matrices/sidebar-matrices/index.html\n"
    "data: "
)

# The tree of matricies on /matrices/
matrices = [
    {
        "name": "Enterprise",
        "name_fa": "سازمانی",
        "type": "local",
        "path": "enterprise",
        "matrix": "enterprise-attack",
        "platforms": [
            "Windows",
            "macOS",
            "Linux",
            "PRE",
            "Office Suite",
            "Identity Provider",
            "SaaS",
            "IaaS",
            "Network Devices",
            "Containers",
            "ESXi",
        ],
        "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> Matrix for Enterprise.",
        "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که ماتریس سازمانی MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند.",
        "subtypes": [
            {
                "name": "PRE",
                "name_fa": "پیش از حمله",
                "type": "local",
                "matrix": "enterprise-attack",
                "path": "enterprise/pre",
                "platforms": ["PRE"],
                "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> PRE platform. The techniques below take place outside of the victim environment, often as a preparatory measure to support targeting.",
                "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی PRE در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر خارج از محیط قربانی رخ می‌دهند و اغلب به عنوان اقدام آماده‌سازی برای پشتیبانی از هدف‌گیری استفاده می‌شوند.",
                "subtypes": [],
            },
            {
                "name": "Windows",
                "name_fa": "Windows",
                "type": "local",
                "matrix": "enterprise-attack",
                "path": "enterprise/windows",
                "platforms": ["Windows"],
                "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> Windows platform. The techniques below are known to target hosts running Microsoft Windows operating systems.",
                "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی Windows در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر میزبان‌هایی را هدف می‌گیرند که سیستم‌عامل Microsoft Windows را اجرا می‌کنند.",
                "subtypes": [],
            },
            {
                "name": "macOS",
                "name_fa": "macOS",
                "type": "local",
                "matrix": "enterprise-attack",
                "path": "enterprise/macos",
                "platforms": ["macOS"],
                "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> macOS platform. The techniques below are known to target hosts running macOS operating systems.",
                "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی macOS در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر میزبان‌هایی را هدف می‌گیرند که سیستم‌عامل macOS را اجرا می‌کنند.",
                "subtypes": [],
            },
            {
                "name": "Linux",
                "name_fa": "Linux",
                "type": "local",
                "matrix": "enterprise-attack",
                "platforms": ["Linux"],
                "path": "enterprise/linux",
                "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> Linux platform. The techniques below are known to target hosts running Linux operating systems.",
                "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی Linux در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر میزبان‌هایی را هدف می‌گیرند که سیستم‌عامل Linux را اجرا می‌کنند.",
                "subtypes": [],
            },
            {
                "name": "Cloud",
                "name_fa": "ابر",
                "type": "local",
                "matrix": "enterprise-attack",
                "path": "enterprise/cloud",
                "platforms": ["Office Suite", "Identity Provider", "SaaS", "IaaS"],
                "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> cloud platforms.",
                "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوهای ابری MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند.",
                "subtypes": [
                    {
                        "name": "Office Suite",
                        "name_fa": "مجموعه اداری",
                        "type": "local",
                        "matrix": "enterprise-attack",
                        "path": "enterprise/cloud/officesuite",
                        "platforms": ["Office Suite"],
                        "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> Office Suite platform. The techniques below are known to target cloud-based office application suites such as Microsoft 365 and Google Workspace. Office application suites are SaaS platforms that typically combine email, chat, document management, and automation functionality for use in a collaborative environment.",
                        "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی مجموعه اداری در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر مجموعه‌های برنامه اداری ابری مانند Microsoft 365 و Google Workspace را هدف می‌گیرند.",
                        "subtypes": [],
                    },
                    {
                        "name": "Identity Provider",
                        "name_fa": "ارائه‌دهنده هویت",
                        "type": "local",
                        "matrix": "enterprise-attack",
                        "path": "enterprise/cloud/identityprovider",
                        "platforms": ["Identity Provider"],
                        "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> Identity Provider platform. The techniques below are known to target cloud-based identity-as-a-service (IDaaS) platforms such as Microsoft Entra ID and Okta. Identity providers are SaaS platforms that support identity management and single sign-on across multiple applications.",
                        "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی ارائه‌دهنده هویت در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر سکوهای هویت به عنوان سرویس مانند Microsoft Entra ID و Okta را هدف می‌گیرند.",
                        "subtypes": [],
                    },
                    {
                        "name": "SaaS",
                        "name_fa": "SaaS",
                        "type": "local",
                        "matrix": "enterprise-attack",
                        "path": "enterprise/cloud/saas",
                        "platforms": ["SaaS"],
                        "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> SaaS platform. The techniques below are known to target cloud-based software-as-a-service (SaaS) platforms. SaaS encompasses cloud-hosted applications with a variety of functionality.",
                        "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی SaaS در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر سکوهای نرم‌افزار به عنوان سرویس ابری را هدف می‌گیرند.",
                        "subtypes": [],
                    },
                    {
                        "name": "IaaS",
                        "name_fa": "IaaS",
                        "type": "local",
                        "matrix": "enterprise-attack",
                        "path": "enterprise/cloud/iaas",
                        "platforms": ["IaaS"],
                        "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> IaaS platform. The techniques below are known to target cloud-based infrastructure-as-a-service (IaaS) platforms. IaaS encompasses cloud-hosted infrastructure, such as virtual machines, object storage, databases, and serverless functionality.",
                        "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی IaaS در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر سکوهای زیرساخت به عنوان سرویس ابری را هدف می‌گیرند.",
                        "subtypes": [],
                    },
                ],
            },
            {
                "name": "Network Devices",
                "name_fa": "دستگاه‌های شبکه",
                "type": "local",
                "matrix": "enterprise-attack",
                "path": "enterprise/network-devices",
                "platforms": ["Network Devices"],
                "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> Network Devices platform. The techniques below are known to target network devices such as routers, switches, and load balancers.",
                "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی دستگاه‌های شبکه در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر دستگاه‌هایی مانند روترها، سوییچ‌ها و متعادل‌کننده‌های بار را هدف می‌گیرند.",
                "subtypes": [],
            },
            {
                "name": "Containers",
                "name_fa": "کانتینرها",
                "type": "local",
                "matrix": "enterprise-attack",
                "path": "enterprise/containers",
                "platforms": ["Containers"],
                "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> Containers platform. The techniques below are known to target containers and container orchestration systems such as Kubernetes.",
                "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی کانتینرها در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر کانتینرها و سامانه‌های هماهنگ‌سازی کانتینر مانند Kubernetes را هدف می‌گیرند.",
                "subtypes": [],
            },
            {
                "name": "ESXi",
                "name_fa": "ESXi",
                "type": "local",
                "matrix": "enterprise-attack",
                "path": "enterprise/esxi",
                "platforms": ["ESXi"],
                "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> ESXi platform. The techniques below are known to target VMware ESXi hypervisors. The Matrix contains information for the ESXi platform.",
                "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی ESXi در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر هایپروایزرهای VMware ESXi را هدف می‌گیرند.",
                "subtypes": [],
            },
        ],
    },
    {
        "name": "Mobile",
        "name_fa": "موبایل",
        "type": "local",
        "matrix": "mobile-attack",
        "path": "mobile",
        "platforms": ["Android", "iOS"],
        "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> Matrix for Mobile. The Matrix covers techniques involving device access and network-based effects that can be used by adversaries without device access.",
        "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که ماتریس موبایل MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. این ماتریس تکنیک‌های مرتبط با دسترسی به دستگاه و اثرهای مبتنی بر شبکه را پوشش می‌دهد که مهاجمان می‌توانند بدون دسترسی به دستگاه از آن‌ها استفاده کنند.",
        "subtypes": [
            {
                "name": "Android",
                "name_fa": "Android",
                "type": "local",
                "matrix": "mobile-attack",
                "path": "mobile/android",
                "platforms": ["Android"],
                "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> Android platform. The techniques below are known to target mobile devices running Android operating systems.",
                "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی Android در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر دستگاه‌های موبایلی را هدف می‌گیرند که سیستم‌عامل Android را اجرا می‌کنند.",
                "subtypes": [],
            },
            {
                "name": "iOS",
                "name_fa": "iOS",
                "type": "local",
                "matrix": "mobile-attack",
                "path": "mobile/ios",
                "platforms": ["iOS"],
                "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> iOS platform. The techniques below are known to target mobile devices running iOS operating systems.",
                "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که سکوی iOS در MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند. تکنیک‌های زیر دستگاه‌های موبایلی را هدف می‌گیرند که سیستم‌عامل iOS را اجرا می‌کنند.",
                "subtypes": [],
            },
        ],
    },
    {
        "name": "ICS",
        "name_fa": "سامانه‌های کنترل صنعتی",
        "type": "local",
        "path": "ics",
        "matrix": "ics-attack",
        "platforms": [],
        "descr": "Below are the tactics and techniques representing the MITRE ATT&CK<sup>&reg;</sup> Matrix for ICS.",
        "descr_fa": "در ادامه تاکتیک‌ها و تکنیک‌هایی آمده‌اند که ماتریس سامانه‌های کنترل صنعتی MITRE ATT&CK<sup>&reg;</sup> را نمایش می‌دهند.",
        "subtypes": [],
    },
]

deprecated_matrices = [
    {
        "name": "PRE-ATT&CK",
        "matrix": "pre-attack",
        "path": "pre",
    }
]

platform_to_path = {
    "PRE": "enterprise/pre",
    "Windows": "enterprise/windows",
    "macOS": "enterprise/macos",
    "Linux": "enterprise/linux",
    "Office Suite": "enterprise/cloud/officesuite",
    "Identity Provider": "enterprise/cloud/identityprovider",
    "SaaS": "enterprise/cloud/saas",
    "IaaS": "enterprise/cloud/iaas",
    "Network Devices": "enterprise/network-devices",
    "Containers": "enterprise/containers",
    "ESXi": "enterprise/esxi",
    "Android": "mobile/android",
    "iOS": "mobile/ios",
}

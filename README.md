# Web Scraping Project

Web Scraping project for Independent Study (under Prof. Rahul Chatterjee) at UW Madison - Spring 2020, continuted into Fall 2020.

The original scraper has been broken down into components:-
1. newScraper: which starts the initial scraping, it is also responsible for parsing the arguments passed to the script
2. utility: responsible for reading the seed search terms
3. databaseUtility: driver functions for database operations
4. parserUtility: have dedicated parsing functions for support of all individual websites

Base Unique Search Terms - 1557

| Name          | Link | OS  | Language |Number of Queries  | Issue Faced |Completed|Number of Apps Retreived|
| --------------| ---- | --- | ---------|-----------------------|-------------|---------|------------------------|
|Apkcombo| https://apkcombo.com|Android|English, Arabic, Spanish & More|0|Blocking due to cloudflare|No|0
Apkpure Com|https://apkpure.com|Android|English|1557||Yes|3470(distinct apps)|
APK Downloader (Apk-dl)|https://apk-dl.com|Android|English|1557||Yes|4133(distinct apps)|
Hiapkdownload|https://www.hiapkdownload.com/|Android|Arabic|| Only Arabic Search| No |0|
Apkmonk|https://www.apkmonk.com|Android|English||Cloudflare Error|No|0|
Happymod|https://www.happymod.com|Android|English||||
Apkpure Ai|https://apkpure.ai/|Android|English||||
APK Support|https://apk.support/|Android|English| Approx 2500 || Yes | 127616|
APK Turbo|https://www.apkturbo.com/|Android|English|0|Blocking due to cloudflare|No|0
Android Apps APK|https://androidappsapk.co/|Android|English||||
AppPure (iPhone Apkpure)|https://iphone.apkpure.com|iOS|English||||
Android APK|https://android-apk.org/|Android|English|0|1. No Website search|No|0|
Qimai|https://www.qimai.cn/|iOS & Android|Chinese|0|1. Webiste is in different language|No|0|
APK Follow|https://www.apkfollow.com|Android|English|0|1. Captcha required, not able to access through script|No|0|
APK Plz|https://apkplz.net|Android|English|1557|1. No related search term|Yes|24(distinct apps|
APKTADA|https://apktada.com|Android|English|1557|1. No related search term|Yes|40(distinct apps)|
APKsFULL|https://apksfull.com|Android|English||||
APK.CO|https://apk.co|Android|English|0|1. Search Not Working|No|0|
AllFreeAPK|https://m.allfreeapk.com|Android|English|1557|1. No related search term|Yes|22471(distinct apps)|
APK Plus|https://apk.plus|Android|English|||
Droid Informer|https://droidinformer.org/|Android|English||||
APK Dom|https://apkdom.com|Android|English|0.|1. Website HTML change when access by python script instead of browser|No|0
Apptopia|https://apptopia.com|Android|English|0|1. Not a app website|No|0|
App Annie|https://www.appannie.com|Android|English|0|1. Not a app website|No|0|
APK Live|https://apks.live|Android|English|0|1. No Website search|No|0|
AppChoPC|https://appchopc.com|Android|Vietnamese|0|1. No Website search|No|0|
Hack-Cheat|https://hack-cheat.org|Android|English|0|1. No Website search|No|0|
Apkandroid_RU|https://www.apkandroid.ru|Android|Russian|0|1.Website is in different language|No|0|
Freeapkbaixar|https://www.freeapkbaixar.com|Android|Portuguese|0|1. Website is in different language|No|0|
Freeapk.id|https://www.freeapk.id|Android|Indonesian|0|1.Website is in different language|No|0|
Deepaso|https://www.deepaso.com|iOS|English|0|1. Not a app website|No|0|
APK Fab|https://apkfab.com|Android|English|1557|1.No related search term|Yes|10692(distinct apps)|
Malavida|https://www.malavida.com|iOS & Android|English, Spanish, German, Russian, French, Portuguese, Japanese & Italian|1557|1. No Related Search Term|Yes|363(distinct apps)
APK GK|https://apkgk.com/|Android|English|1557|1. No related search term| Yes|5889(distinct apps)|
APK Clean|https://apkclean.net/|Android|English|0|1. No website search|No|0|

   


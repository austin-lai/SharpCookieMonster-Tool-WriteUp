# SharpCookieMonster - Tool - WriteUp

> Austin Lai | October 31st, 2022

---

## Table of Contents

<!-- TOC -->

- [SharpCookieMonster - Tool - WriteUp](#sharpcookiemonster---tool---writeup)
    - [Table of Contents](#table-of-contents)
    - [Description or Introduction](#description-or-introduction)
    - [Building SharpCookieMonster](#building-sharpcookiemonster)
        - [Merge WebSocket4Net using ILMerge](#merge-websocket4net-using-ilmerge)
    - [Testing SharpCookieMonster](#testing-sharpcookiemonster)
        - [Here our mini demo](#here-our-mini-demo)
        - [Using SharpCookieMonster with execute-assembly command from cobaltstrike beacon.](#using-sharpcookiemonster-with-execute-assembly-command-from-cobaltstrike-beacon)
        - [Evaluate SharpCookieMonster Usability](#evaluate-sharpcookiemonster-usability)
            - [**SharpCookieMonster with Python and Selenium**](#sharpcookiemonster-with-python-and-selenium)
                - [**cookiex.py**](#cookiexpy)
    - [Conclusion](#conclusion)

<!-- /TOC -->

## Description or Introduction

<!-- Description -->

[SharpCookieMonster](https://github.com/m0rv4i/SharpCookieMonster) is a C# project will dump cookies for all sites, even those with httpOnly/secure/session flags.

It can be used with C2 such as cobaltstrike with `execute-assembly`.

However, for this write up; we going to test and understand how it can be used with cobaltstrike.

<!-- /Description -->

<br>

## Building SharpCookieMonster

We start off with cloning the repo using command below:

`git clone https://github.com/m0rv4i/SharpCookieMonster.git`

![](/assets/images/2022-10-15-10-48-15.png)

It is a Visual Studio Solution Project.

![](/assets/images/2022-10-15-10-43-56.png)

Let's open with Visual Studio, expand the `solution` and right-click `references`.

![](/assets/images/2022-10-15-10-52-49.png)

Then select `Manage NuGet Packages...`.

![](/assets/images/2022-10-15-10-53-46.png)

You will notice the `NuGet Package Manager` panel showing the following prompt/error message.

![](/assets/images/2022-10-15-10-54-53.png)

It showing the `ILMerge` and `WebSocket4Net` packages are missing.

You will need to download the packages with **correct version stated** from <nuget.org> and install it manually.

For `ILMerge`, you can go to <https://www.nuget.org/packages/ilmerge/3.0.29> and download it.

![](/assets/images/2022-10-15-10-59-22.png)

Same goes for `WebSocket4Net, refer to <https://www.nuget.org/packages/WebSocket4Net>.

![](/assets/images/2022-10-15-11-01-04.png)

The downloaded packages are `.nupkg` files

![](/assets/images/2022-10-15-11-02-28.png)

Once we have the files, we will need to configure Visual Studio to use them as package source by clicking the `Setting|Options` button bring up `Package Source` configuration page as shown below:

![](/assets/images/2022-10-15-11-05-06.png)

On `Package Source` page, click the `add` button on top right.

![](/assets/images/2022-10-15-11-06-32.png)

It will automatically select and fill the information, however you will need to change it manually for `Source` path to where the `nupkg` file is located. You can also given a specific name for this new sources.

![](/assets/images/2022-10-15-11-08-54.png)

Once you have finished, click the **update** button to update the package source configuration.

![](/assets/images/2022-10-15-11-11-53.png)

It will reflect correctly

![](/assets/images/2022-10-15-11-12-19.png)

Once you done, just hit `OK` to close the configuration page.

In the `NuGet Package Manager` page, you will need to change the `Package Source` to the `LocalFiles` or whatever name you have given in previous steps. Once you have changed, click the `Restore` button just right up. It will autumatically resolved the missing packages issue.

![](/assets/images/2022-10-15-11-15-10.png)

Now we are good to go and build `SharpCookieMonster` by going to the `Build` tab and select `Build Solution` or you can use the shortcut of `Ctrl+Shift+B`.

![](/assets/images/2022-10-15-11-18-08.png)

There will be `Output` panel showing you have successfully built the `SharpCookieMonster`.

![](/assets/images/2022-10-15-11-18-52.png)

And `voila` we have our `SharpCookieMonster` binary.

![](/assets/images/2022-10-15-11-19-40.png)

<br>

### Merge WebSocket4Net using ILMerge

As the creator of `SharpCookieMonster` mentioned under section <https://github.com/m0rv4i/SharpCookieMonster#building>, we will need to merge `WebSocket4Net.dll` using `ILMerge` **in order to use WebSockets to communicate with Chrome**

Since we have `ILMerge` installed with `SharpCookieMonster`, it is located under the `packages` folder as shown below:

```
YOUR_SharpCookieMonster\packages\ILMerge.3.0.29\tools\net452
```

![](/assets/images/2022-10-15-12-16-26.png)

The `WebSocket4Net.dll` is located under the same folder as `SharpCookieMonster` binary.

![](/assets/images/2022-10-15-12-20-45.png)

To merge the `WebSocket4Net` library, first we need to rename the original `SharpCookieMonster` binary.

Then run the following command to merge the library:

```
ILMerge.exe /targetplatform:"v2,C:\Windows\Microsoft.NET\Framework\v2.0.50727" /out:SharpCookieMonster.exe SharpCookieMonsterOriginal.exe WebSocket4Net.dll
```

Here is the new `SharpCookieMonster` binary.

![](/assets/images/2022-10-15-12-22-41.png)

<br>

## Testing SharpCookieMonster

We have spined up Windows VM and install Google Chrome with testing user signed-in to `Gmail|Google|Chrome`.

For **testing purposes**, we need to add `Download` folders into Windows Defender Exclusion.

![](/assets/images/2022-10-15-11-34-17.png)

We also transfer `SharpCookieMonster` binary to the VM using python `updog`.

![](/assets/images/2022-10-15-12-31-29.png)

Now we can use `SharpCookieMonster` against any site to extracts cookies on the Windows VM with the command shown below:

```
SharpCookieMonster.exe https://www.google.com
```

<br>

### Here our mini demo

![](/assets/images/demo1-1.gif)

<br>

### Using SharpCookieMonster with `execute-assembly` command from cobaltstrike beacon.

First, let's start cobaltstrike teamserver.

![](/assets/images/2022-10-15-19-51-20.png)

Then, we connect cobaltstrike's client to teamserver.

![](/assets/images/2022-10-15-20-15-41.png)

Next, create `http` listener binding port `80` on cobaltstrike teamserver's IP.

![](/assets/images/2022-10-15-20-21-01.png)

Next, create `Scripted Web Delivery (Powershell)` payload as shown below:

![](/assets/images/2022-10-15-20-22-23.png)

Run the powershell payload generated from the previous step inside Windows VM.

![](/assets/images/2022-10-15-20-24-56.png)

And we got a callbacked on cobaltstrike from the beacon.

![](/assets/images/2022-10-15-20-25-22.png)

Now we use `execute-assembly` command from cobaltstrike to execute the `SharpCookieMonster` binary, below is our mini demo.

![](/assets/images/cobaltstrike-sharpcookiemonster.gif)

<br>

### Evaluate SharpCookieMonster Usability

As shown below, the <span style="color:green">**Left Green Arrow**</span> are the cookies extracted from Google Chrome and the <span style="color:red">**Right Red Arrow**</span> are the cookies extracted using SharpCookieMonster.

![](/assets/images/2022-10-19-103418.png)

The cookies json objects and formats extracted using SharpCookieMonster **not the updated** cookies objects and formats from Chrome.

Cookies <span style="color:green">**Left Green Arrow**</span> that extracted from Google Chrome can be used and imported into attacker machines without any issue and the session is valid.

However, cookies extracted using SharpCookieMonster show in the <span style="color:red">**Right Red Arrow**</span> panel cause session invalid and some cookies objects are unable to be imported due to the different formats and cookies objects extracted.

<br />

#### **SharpCookieMonster with Python and Selenium**

We run some tests and researches on how the cookies extracted from SharpCookieMonster that can be imported and re-used in actual red team engagement.

After a few tests, we finally figured out that cookies extracted using SharpCookieMonster can be imported with Python and Selenium.

We started to build the script called [cookiex.py](https://github.com/austin-lai/SharpCookieMonster-Tool-WriteUp/blob/master/cookiex.py).

<br />

##### **[cookiex.py](https://github.com/austin-lai/SharpCookieMonster-Tool-WriteUp/blob/master/cookiex.py)**

There are several python packages to be installed and used in the script:

- [pip3 install undetected-chromedriver](https://pypi.org/project/undetected-chromedriver/)
- [pip3 install selenium](https://pypi.org/project/selenium/)
- `pip3 install getpass`
- `os`
- `json`
- `time`
- `pickle`

<br />

## Conclusion

**SharpCookieMonster** can be used to extract cookies from Google Chrome, however due to the updated Google Chrome's cookies structure and objects; `SharpCookieMonster` unable to extract the correct structure. Hence, it is failed to achieve our objective.

> [!IMPORTANT]
> This branch is temporary.<br>
> The purpose of this section is to implement a different logic for displaying active time.<br>
> (But there's a problem...)<br>
<details>
<summary> What's the problem? </summary><br>
The problem is that Discord (or, more specifically, pypresence)<br>
has a limit on the interval between activity updates… which means it won’t be possible to display the time every second...<br>

<b>So what was my plan?</b><br>

I wanted my "app" to detect when the user launched the desired app and immediately display that time in the corresponding activity...<br>

But I didn’t take into account that if you don’t specify the time when sending an activity, the timer resets...
And displaying the time every 5 seconds (or so) isn’t very "aesthetic".

So I’ve temporarily decided to split the app into different versions… maybe in the future I’ll find another way to "synchronize" the time in the activity...
</details>

> [!NOTE]
> Maybe someday I’ll explain how to use it, but for now, let’s leave it at that.<br>
> In the meantime, you can try figuring it out on your own (it really isn't that hard)<br>

## Project Roadmap (in the near future):
- Write a clear and simple README (if only there were more words...)
- <s>Implement Windows notifications</s>
- <s>Implement hotkeys to enable/disable activity</s>
- Design a user interface (maybe?)
- Automatic updates via GitHub (possible, necessary?)
- Automatic shutdown upon detection of other activity (is this possible?)
- Support for multiple languages (lower priority)

## Inspired by
The idea that inspired me to write this script comes from: <a href=https://vencord.dev/plugins/CustomRPC>CustomRPC</a>

The difference is that this script is dynamic and allows you to create an unlimited number of different activities (and it also doesn't require installing <a href=https://github.com/Vendicated/Vencord>Vencord</a>)

## Disclaimer
Discord is trademark of Discord Inc. and solely mentioned for the sake of descriptivity.<br>
Mention of it does not imply any affiliation with or endorsement by Discord Inc.


## Using this script does not violate Discord's Terms of Service. (I think?)
> [!NOTE]
> Technically, this isn't a client modification, since you're essentially just running an "app."

> [!IMPORTANT]
> However, if your account is very important to you and having it blocked would be a disaster, you probably shouldn't use any modifications.
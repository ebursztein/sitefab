---
template: blog_post
title: "Full(er) House: Exposing high-end poker cheating devices"
category: security

microdata_type: BlogPosting
lang: en
hidden: false

tags: 
  - machine learning
  - anti fraud and abuse
  - offensive technologies

seo_keywords: 
 - poker cheating
 - poker player
 - card cheating
 - cheating at poker

creation_date: 21 oct 2016 00:00
update_date: 20 nov 2016 02:00

permanent_url: blog/security/fuller-house-exposing-high-end-poker-cheating-devices

banner: /static/images/banner/fuller-house-exposing-high-end-poker-cheating-devices.jpg

authors:
  - Elie, Bursztein

abstract: This post exposes how real-world highly advanced poker cheating devices work.

---
This post exposes how real-world highly advanced poker cheating devices work.

In 2015, I stumbled upon a post in an underground forum, discussing how someone was ripped off at a poker table by a very advanced poker cheating device. From what I understood at that time, the post being in Chinese, the device was able to remotely read card markings to inform the cheater who will win the next hand. 

Intrigued, I decided to follow the trail of this fabled device to see if people were indeed cheating at poker using devices that would fit naturally into a James Bond movie.

Without spoiling too much of the rest of this post, let’s just say that the high-end cheating device that I was able to get my hands on far exceeded my expectations and it really is an outstanding piece of technology.

As a matter of fact, it is so advanced and cool that with [Celine](http://www.celine.im) and [Jean-Michel](http://blog.j-michel.org/), my co-conspirators, we decided to do a Defcon talk about how it works. You can watch the recording of our talk below and grab [the slides here](https://www.slideshare.net/elie-bursztein/cheating-at-poker-james-bond-style):

[Cheating at poker James Bond style Defcon talk recording](https://youtu.be/bRgCvCTG_XQ)

Due to the complexity and length of the subject, the analysis of the device is split into three blog posts: This post covers how the device works including an overview of it, its software interface, a teardown of the hardware and a look at card markings. [The next post](https://www.elie.net/blog/security/royal-flush-an-in-depth-look-at-poker-cheating-devices-accessories), look at how the device accessories work. The last post will be about how to detect and potentially counter cheating device while playing poker.

Before delving into the inner workings of the device, here is a short demo of it in action to show you how fast and accurate it is at remotely reading cards. Note that I did a fair shuffle and drew the cards at random. There was no sleight of hand involved.

[Poker cheating device demo](https://youtu.be/coY2Lrd_AIE)

## Acquiring the device

![Poker cheating reseller](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/poker-cheating-device-reselller.jpg)

Finding a few more posts on English forums convinced me that those devices were real and gave me clue of what I was looking for. I was able to find a few potential online sellers, including the one depicted in the screenshot above.

The problem with all the sellers I found  was that the price was very steep ($5000!) and there was very little description whatsoever of how the device operates. If I hadn’t been confident the device existed, I would have assumed it was a scam. 

Inspecting the few screenshots of the device available on resellers websites, allowed me to figure out who was the manufacturer of the device: a factory located in China. I decided to take my chances and contact them directly.

After a few rounds of negotiation, I was able to acquire the device, some accessories and a few marked decks for roughly $1300 thanks to the help of my Chinese contacts. While still expensive, going straight to the device maker was still way cheaper than the online re-seller and guaranteed that I got the real deal. That is, after I took a leap of faith and sent them the money via Western Union :)

## Device overview
![Poker cheating device side view](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/poker-device.jpg)

Upon ordering the poker cheating device I kinda expected, based on the screenshots I had seen early on, to get a dedicated piece of hardware that kinda looked like a fake phone. However, to my surprise, the device, showcased in the picture above, far exceeded my expectations by being a fully functional phone with extra hardware dedicated to cheating. Also to my surprise, the device not only allows to cheat at Poker but to cheat at almost any kind of card games you can think of.

Using a modified phone as a cheating device offers the key advantage that it is impossible to tell that it is a cheating device unless you know what to look for. It is also a decent smartphone that can make phone calls and run all the apps you love.

![Real phone](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/real-phone.jpg)

In term of exterior appearance, the device appears to be a knock-off of a popular phone, which is depicted in the photo above. Like the Core, the device has 8GB of storage and 1GB of RAM. Overall, the quality of the device clearly indicates that high-end poker cheating devices comprise a very lucrative and organized black market.

## Software

Upon powering up the device, the familiar interface loads up and the only potential tell that this phone might be special is that it runs with a custom Chinese 4.2.2 ROM. 

The hardware used for cheating is controlled by a custom Android app through a custom kernel module. Outside of the dedicated app, there is no way to interact with the cheat hardware. This section showcases how the phone app works from the user’s perspective.

Note that taking a screenshot of the cheating app turned out to be more difficult than expected because the ROM is hardened against analysis. In particular, they removed the ADB server (Android debugging) and the ability to take a screenshot when the phone is operating in cheating mode. However, with a bit of work, I was able to re-establish the functionalities needed to take the screenshots of the app used in this section.

![Phone app menu](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/android-menu.jpg)

As visible in the screenshot above, the cheating interface appears in the app menu as a normal Android app that is simply named “game”.

![App login](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/game-app-login.jpg)

Upon launching the app, you are greeted by a password prompt. As a security measure against the device being lost in transit, this password is communicated to the buyer only when they have confirmed that they have received the device. Ironically, there is a hardcoded backdoor password in the app, which makes this security measure pointless if you know the backdoor password.

![App main menu](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/game-app-main-screen.jpg)

The main menu has six main icons as visible in the screenshot. The most important ones are: the game hall, which allows you to activate or buy more games; the settings menu, which allows you to configure the device; and the purchased screen, which activates the cheating device for a given game. Let’s look at these three in turn.

![App game selection](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/game-hall.jpg)

The game hall menu lists all the games supported by the device with a basic description of each. In total, there are hundreds of supported games, which supports the hypothesis that high-end cheating devices are used not only for poker but any form of gambling that involves cards.

![App settings](https://www.elie.net/image/public/1476982328/game-app-settings.jpg)

The settings screen allows you to configure, among other things, connections to accessories (covered in the next post) and how the prediction of the winner is reported. For example, the device can continuously tell you who is winning or tell you only once.

![App purchase screen](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/purchased.jpg)

The purchased screen, visible above, allows you to select which game the device will analyze. Note at the top of the screen the typo, which shows that the interface was rushed out. 

Originally based on my investigation, I thought these devices were mostly used in Asia, which could explain the poor translation. However, following the Defcon talk, anonymous sources told me that these devices are indeed actively used in the US, including Vegas, to rip people off.

![Cheating screen](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/game-capture.jpg)

Upon clicking on a game, you end up in the main cheating screen, showcased in the screenshot above. The top half of the screen displays a view of the deck as seen by the secret camera embedded in the device. The image is rotated by -90 degree with the top of the deck being on the left and the bottom on the right. This image is mainly used to adjust the device relative to the deck to ensure the cards are read accurately. With a little practice, it is actually fairly easy to position the device without the help of the camera view.

The bottom half of the deck shows various bits of information, including the game type (1016 in our case), the number of players (which can be changed during a poker game with the volume buttons), if the haptic feedback device is connected and the current result. In the screenshot, the result is “H6, D8,” which implies that the top card is the six of hearts and the second one is the eight of diamonds.

Before discussing how the device is able to read cards remotely, it is worth noting that the camera and decoding the cards are handled in the kernel module, which is written in C. The app merely reads this information and interprets it.


## How the device works

![How poker cheating devices work](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/how-poker-cheating-devices-work.jpg)

As depicted in the diagram above, to read cards remotely, the device has a hidden camera embedded on one side. The infrared (IR) filter has been removed so it can perceive IR light. Next to it, there are three concealed IR LEDs that illuminate the deck to make the markings on the cards visible to the camera. 

![Cheating device under normal light condition](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/ir-led-outside-light.jpg)

A neat trick is that the phone housing is made of IR passband plastic: while the side of the phone appears to be solid and opaque, in reality it allows IR light to pass through. 

![Cheating device under low light conditions](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/ir-led-outside-dark.jpg)

The best way to illustrate this behavior, as visible in the photo above, is to take a picture of the device while it is powered on in the dark with a camera with no IR filter. Doing so, as you can see, the three LEDs are clearly visible. The cool thing is that phone cameras are somewhat sensitive to IR light, so pointing your phone camera at a poker cheating device will show the huge blast of light.

## Card markings
![How the cheating device see the cards](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/marked-vs-regular.jpg)

What makes the whole thing work is the use of a special deck in which the four edges of each card are marked with IR-absorbing ink. As a result, when this marked deck is illuminated by the IR LEDs, the spots of ink absorb the IR, creating a sequence of black spots, as visible in the photo above. This can be compared with a regular deck, which shows no markings when illuminated with IR, as visible in the photo as well. 

![Cards marking](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/card_marking.png)

The sequence of black spots created by the IR illumination, illustrated in the photo above, is read remotely by the cheating device to infer a card’s suit and value. You can think of those markings as invisible barcodes. 

![Cards marking annotation](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/card-encoding-2.jpg)

Each card has a unique code, as visible in the photo above, which shows the markings for the six of hearts, six of clubs, six of diamonds, five of diamonds and five of hearts. These markings are repeated on each side of a card. Originally, we thought there was some sort of order but it turns out that the marking only encodes a known value for each card. We suspect that the values were chosen to maximize the accuracy of the reader, potentially something like a [Gray code](https://en.wikipedia.org/wiki/Gray_code).

![Marked cards](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/deck.jpg)

An interesting question is how they get the markings onto the cards. At first, I would have ventured that they would create a deck from the ground up, but after closely inspecting a few decks, it is clear that they use a real Bicycle deck (or any brand you want) and use a dedicated machine to mark them. 

As observed by an anonymous source, this marking process leaves a very subtle yet visible sign: the corners of the cards are slightly cut. We believe it is to help with the marking process.

![Marked decks are sealed](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/deck-box.jpg)

When you order a pack of marked cards, it is shipped with its seal and plastic wrap “intact,” as visible in the photo above. This makes the victims of the scam less suspicious, as the pack can be opened in front of their eyes. 

![Marked deck box bottom](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/marked-deck-box-cutted-open.jpg)

However, the way the seal is preserved is less than ideal: instead of tampering with the seal and replacing it (an easy feat!) they opted to cut the bottom of the box as highlighted in the photo above. This can be easily spotted by looking at the card box, whereas tampering with the seal would have been invisible.

## Complexity

To truly appreciate how amazing this cheating device is, it is worth highlighting some of the key but not obvious challenges faced when using high-end technology to cheat at cards.

On top of the need to develop custom hardware and a card-marking process, accurately reading cards in real time is complex for three additional reasons:

1. The algorithm has to realign the reading to compensate for a card’s position (angle and rotation) and deal with potentially misaligned or bent cards. 

2. The reading and decoding have to be fast, which on an underpowered phone is not trivial. Given this need for speed, it is not surprising that the entire recognition algorithm was implemented in C and not Java.
3. Cards are very thin, which means their markings are only a few pixels tall. Reading those with a low-resolution camera from a distance of 30 cm leaves little room for error.

##Demo
Here is an exposed view demo of the poker reader in action, which shows what the device sees when I put the deck on the table and showcase how fast it is at detecting the cards:

[Poker cheating device exposed](https://youtu.be/Nn5C9HmHt_4)

## Hardware teardown

Now that we know how the device works, let’s see how it is implemented in hardware by tearing the device down.

![Device teardown](/static/images/images/fuller-house-exposing-high-end-poker-cheating-devices/device-inside.jpg)

Removing the enclosure reveals, as visible in the photo above, that the secret camera is connected to a dedicated chip. Removing the black tape on the top left corner reveals the IR LEDs, as visible in the screenshot below.

Note the RF and Bluetooth antenna connectors on the right side of the phone. These are controlled by the dedicated chip as well and are used to communicate with the accessories. RF is used to connect the remote camera and the remote control, while Bluetooth is used to connect to the audio and haptic output devices. Those accessories are discussed in this [next post](https://www.elie.net/blog/security/royal-flush-an-in-depth-look-at-poker-cheating-devices-accessories).

## Conclusion
High-end poker cheating devices are real and highly efficient. The complexity and the build quality of these devices as well as the number of games they support indicate that there is a very profitable and active black market for gambling cheating devices. For more information on Poker cheating devices, you can read [the next post of the series about device accessories](https://www.elie.net/blog/security/royal-flush-an-in-depth-look-at-poker-cheating-devices-accessories).

Thanks for reading this post to the end! If you enjoyed it, don’t forget to share it on your favorite social network so your friends and colleagues can too.

To get notified when the next post is online, follow me on [Twitter](https://twitter.com/elie), [Facebook](https://www.facebook.com/elieblog), [Google+](https://plus.google.com/+ElieBursztein). You can also get the full posts directly in your inbox by subscribing to my mailing list or the [RSS feed](http://feeds.feedburner.com/inftoint).
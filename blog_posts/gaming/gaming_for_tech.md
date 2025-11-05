# Background

- Most of my network is in healthtech or tech
- Many people are curious about gaming industry
- I have a little experience in the gaming industry (but not a lot) so hopefully I can clear up some things
- I had a number of misconceptions about gaming that others may have too
- Singularity 6 / Palia for about a year

My background with gaming goes back to my early childhood, as does my background with programming. I still remember playing Atari games and my first experiences with programming on the VIC-20. And later I have many more fond memories of the NES and SNES.

If I remember right, my first programming book was about gaming but I was far too ambitious. So I set that aside for a while and learned programming on and off, more in high school. 

Much later, I went to college at TCNJ for computer science. I'd learned that programming was complicated enough that I needed to learn a lot before trying to build anything. Then later in the program, I heard an exciting story: A classmate got an internship in the gaming industry! But when I asked more, I found that they mostly were there to get coffee for "real" developers. Not long after that, I started to see stories like the EA spouse one which sounded horrific. So I set that dream aside.


# About this post

In scope: FAQ-like topics

Out of scope: 
- Things that are very similar across industries
- I won't talk as much about topics that we're my area of focus

# Crunch mode and Chaos

The gaming industry has a reputation for crunch mode: If a team is behind schedule and headed towards a deadline, the team may work much longer hours to try and meet their goals. I was generous in phrasing it as a democratic team choice when it can often come from pressure from higher ups.

My impression from S6 is that and the Doublefine documentaries is that:
1. It's popular to say "we don't crunch": In essence, the older generation of devs that are now leaders are saying "never again" to the bad experiences they had
2. Crunching is less extreme than it was 20 years ago (but newer devs don't have that history)

At S6 I often observed how gaming veterans reacted to different situations. Most of them were very disciplined with time management, and some tolerated a small amount of crunch. Younger devs tended to opt-in to crunching more. Some producers (read: PMs) tended to encourage crunching while others didn't.

Now to the interesting part: Why do gaming companies tend to crunch, and is it avoidable?

I'll start with my answer then the explanation: 
- Some chaos is avoidable
- Some chaos is unavoidable
- Crunching is one response to chaos

Let me give a few examples of avoidable chaos first:
- There's too much work for the team to do in the scheduled time
- The game will support PC and Nintendo Switch, but the design requirements of Switch are not taken into account during initial development
- The game is designed to not be latency-sensitive, but a latency-sensitive feature is added

I tried to pick examples that would be relatable to folks in the tech industry. We're very familiar with having too much work for the scheduled time, and that can often be mitigated without working people harder.

TO ADD
- weak prioritization, ‘DM-driven decision making,’ or managers learning on the job

The example of requirements is something that's knowable (or perhaps even known by some) but not known by the right people. In many cases it can be mitigated by product research and better communication, though not always. 

The third example is another that could be mitigated by better communication. In some cases, it can be mitigated by org structure to encourage the right communication.

Let me also give a few examples of unavoidable chaos:
- The game is more global than expected after launch, causing major changes in priorities
- The game isn't fun

The first example is common in the tech industry. We've all been surprised in some way when launching software, whether more engagement than expected, less engagement, a different kind of engagement, and so on.

The second example is imilar to tech but a little less similar. It's common for early-stage startups to have a product that nobody loves. We'd call that lacking product-market fit, which is a way of saying "hey maybe the product isn't total crap, maybe you just haven't found the right user yet".

In both gaming and tech, once you have something engaging you can refine it. You can interview and survey users to understand what's working and what's not. You can A/B test your ideas for improvements to see if they're effective. There are many, many ways to improve something once you have that foothold.

But game development spends more of the development cycle pre-fun. There's an idea but it's not yet engaging. 

## TODO
- This needs a lot more writing and clarity
- * **“Some of that chaos is unavoidable… it’s part of building a creative work for entertainment.”**
- * Contrast *search* (finding fun) vs *optimize* (SaaS). Show two mini-stories: one where ambiguity produced a great feature; one where avoidable chaos cost a week.
* “The ‘fun’ (timed events) caused the scaling challenge. That’s innovation tax.”
- Because switching costs are so low in gaming, your game has to be really special to do well. That leads to a tendency to innovate and create something new. And that pushes up against the boundaries of what's easy to implement.
- Because there tends to be more chaos in gaming, people adapt and overcome. It's pretty inspiring to see the grit that people bring to problem solving
- Search for literature on "finding the fun"

## Takeaways
- The chaos and crunch mode in gaming can be lessened in well-run companies, but there's always going to be some of it
- There are some similarities to the uncertainty in creating new products, with the key difference that there's no recipe for fun
- Fun is relative to everything else. Playing Tetris for the first time is fun for many people. Playing your 10th Tetris clone is less fun.

## See also
- Psychodessey
- EA spouse


# Tooling

At S6 I spent some time learning Unreal Engine. Initially I was learning by fixing bugs to gain experience for UI polish and features. In that brief time, it felt very similar to mobile development in Android Studio because you're spending a lot of time in a platform-specific IDE with tons of tools and settings. The UI editors felt analagous too.

The biggest point of difference is that UE allows people to edit the game world, defining levels and assets. It even provides a flowchart-based programming language called blueprints. And it's all designed with more customization in mind. In Android, they don't want you modifying the core system. But with Unreal you have the option.

Version control in gaming felt pretty rough (Perforce). In tech most people use git, and it's pretty clear that git alone can't meet the needs of gaming because 1) large binary files need to be versioned and 2) it needs to work for a wide range of employees. While I'm on the subject of version control, let me mention that blueprints didn't have a textual form so you had to screenshot the diffs when submitting your changes for review.

## Takeaways:
- Game development doesn't use git for good reasons
- I wish UE blueprints were more designed with peer review and version control in mind

## See also:
- The software of Palia

## TODO
- Search for a good compare / contrast article

# Internal use aka Dogfooding

Dogfooding is an interesting topic across products and companies:

At Swype, developers were used to loading builds on their phones so we used dev builds all the time. Many other around the company loaded builds on their phones as well. And because we were using our phones so much, we could quickly find out if a new build was an improvement. But that's with the caveat that most of that dogfooding happened in English not other languages. So we sometimes had more bugs in other languages. 

At 98point6, it was tougher to dogfood because we had both software for patients and software for doctors. A virtual healthcare visit required both sides of the software. We'd sometimes do informal tests, but exploratory dogfooding was more reserved for dedicated times when we had multiple people available and had an area of the product we wanted to focus on. Even still, we weren't doctors so our dogfooding of the clinical software wasn't as useful as our dogfooding of the patient software.

At Singularity 6, dogfooding (aka playtesting) needed to be coordinated because it was a multiplayer online game. So we had scheduled weekly playtests for the whole company. Sometimes those playtests had particular themes like a new event, and other times they were less structured.

COMMON THEMES
- Professionals tend to have high-end devices with good internet, and that's often unrealistic
- Dogfooding is effective BUT has limitations for underrepresented groups (e.g., non-English, advanced users)
- Ease of dogfooding has a major effect on bug discovery, etc

Ease of dogfooding:
- S6: The best was internal Steam builds. The worst was when we got last-minute builds that took an hour to download, or had to download a specific version and override the connection strings to a specific server. Switch was much tougher to dogfood as well
- 98point6: The best was when we could use dev or staging. The worst was trying a test on a branch
- Swype: It was pretty easy to test Android builds, but much harder to test iOS builds

## Takeaways and opinions
- Dogfooding is a valuable process in building high quality software, but it has limitations to work around
- Ease of dogfooding has a major effect on bug discovery, etc

# Distribution

These days, games distribution can feel similar to software distribution. Selling a game on Steam is comparable to publishing an Android app on Google Play. The analogy goes pretty deep: Both platforms take a 30% cut of revenue on their platform, have some minimal requirements about what you can publish, and provide some software libraries or services. In both cases you need to optimize your app for the store to make it more visible.

Publishing an app on the iOS App Store is a bit more burdensome due to their manual review process. That can be a good thing for quality and consistency, but the review process can also be inconsistent. We had some frustrating times at 98point6 when a bug fix was blocked because the App Store reviewer was flagging something from a prior version. That introduced delays and degraded the user's experience.

In the gaming world, it's a bit like publishing games for Ninendo Switch. They have a certification process similar in spirit to the iOS process, but it's slower and more involved. I've even heard that the iOS process (including the 30% cut and certification) was inspired by Nintendo's process (CITATION NEEDED). Where the iOS process could take a day or two, the Nintendo process could take several days to a week. 

To give some examples of requirements for a platform like Nintendo:
- Any online chat in the game must be integrated correctly with the Switch's parental controls
- Switch controllers must be referred to as joycons
- ADD ONE MORE

## TODO
The certification cadence of the publisher ends up pushing your development cadence, and that's common outside of gaming as well. When there are longer certification steps, it's too much work to do frequent updates. So it pushes organization to slower, larger updates. That can add extra development overhead because while one version is going through certification, development must continue to start the next version. By the time certification gets back to you, you may not fully remember the previous version. So there's just more to manage.

In contrast, self-publishing applications via the web comes with no such requirements. If you have a bug fix or performance improvement, you can release it right away.

I wanted to bring up this topic because I find that the nuance is often lost in engineering conversations. There's often an oversimplied perspective that changes should be deployed continuously. (TODO: Mention DORA)

Back to the topic of distribution, multi-platform distribution is very similar to non-gaming software:
- You're juggling the competing requirements of each platform and trying to minimize platform-specific work, while recognizing that the importance of some platform-specific work
- You're trying to design a release cadence to balance the constraints of all platforms
- Backend APIs allow you more flexibility in release cadence, but they require extra care to update without client updates

## Takeaways
- Distribution heavily influences release process optimization including the cadence of releases
- Discussion of "what goes in the client vs backend" should really consider release cadence more than it does

Things I prefer from mobile app distribution
- The requirements are usually more clear, and most of them are publicly available
- The certification process is pretty fast

Things I prefer from gaming distribution
- Steam provides from dope APIs, and you're allowed to use them on any platform so long as you publish on Steam

Things I wish were changed
- I wish cert requirements were all public
- I wish all publishers explained the intention of the requirements


# Business stuff

If someone doesn't like your game, they can easily find something better to do with their time. For one, they can easily find another game to try. The switching cost is nearly zero. If you have a free-to-play game, there's even less switching cost.

The closest comparison from the rest of my career was the Swype direct-to-consumer app. People could buy Swype on Google Play for a couple of dollars (which honestly was a tough sell for many on Android). At the time we launched, there weren't that many high quality third party keyboards on Google Play. Depending on your language, it may have even been the only third-party option at the time. Over the years it became more competitive but only a little.

It's even tougher than I've described:
- You might plan your game launch only to be eclipsed by a hit game launching around the same time
- You're not just competing against new releases but also competing against decades of amazing games
- You're not just competing against the same type of game, but many types of games
- You're not just competing against games but other forms of entertainment for some people

## Takeaways
- I have a lot more respect now for developers that succeed financially
- B2B/SaaS companies tend to provide a lot of stability for the team, much more than I ever appreciated
- B2B/SaaS companies in my experience don't need to compete as much on quality. It's much more affected by sales and business relationships

# FTUE

- Because switching costs are low, you have a very short amount of time to hook a player on your game. The same can be true of direct-to-consumer apps, and even in some cases B2B2C apps


When someone uses your app 

* “Onboarding in most apps is straightforward. Games are different—you’re teaching a new grammar.”

* “Tutorial popups are forgettable; quests that *force* you to learn are sticky.”

* “The best FTUE is invisible: you feel like you’re playing, not reading a manual.”

## Takeaways
- The core challenges are similar: Users don't want to read a lot, and want to use your app or play your game ASAP
- Because games have to be fresh and interesting, there's more of a tendency to NEED explanation
- In my opinion, many apps have moved towards a "show don't tell" approach to user training

# Operations

I found it interesting to compare and contrast the operations of 98point6 (24/7 healthcare) to Palia (24/7 gaming). 

At 98point6 we emphasized reliability and scrutinized our service availability. Some years we delivered 99.9%, others closer to 99%. For reference, 99.9% availability means about 9 hours of downtime per year whether planned or unplanned. That's just one or two bad outages per year.

In online gaming it's common to have scheduled downtime. That's a time when the parts of the game may be updated, servers may be restarted, and so on. When things went really well, maybe that would only take 1-2 hours per week (~99% uptime). Coming from healthcare initially I scoffed a bit at the downtime but our tech stack didn't allow much choice but to bring the game down to update all servers and clients at the same time. I'm sure we could've done better in our deployments, whether through more testing, use of feature flags, etc.

It's interesting to think about the difference in scale too: At 98point6 we wanted 99.9% uptime for about 100-1,000 daily active users. At Singularity 6 I wanted 99% update for about 100,000 daily active users. (The numbers are only meant to convey the concept not as references)

My perspective changed over time, seeing that it was really about the expectations of your users. Our players expected Tuesday morning downtime and planned accordingly. It didn't bother most people. What bothered players was unexpected downtime and unexpected instability. So when the 2 hour downtime turned into 4 hours or 6 hours we'd take a lot of heat from players. For those outside of gaming that might sound surprising, after all it's a game right? I found it helpful to remember some of the situations our players had. Some of them were working long hours and only had one day a week they could relax in game. So for them if our outage cut into their weekly time that's a big deal.

## Takeaways
- Scheduled downtime isn't so bad, so long as it's very clear to all your users
- Gaming fills an important role in some people's lives so downtime can be very disruptive

## TODO
- I wonder if this also leads to the tendency to "just reboot the servers" in gaming

# User feedback

First let me just mention the type and scale of feedback across former employers, and I'll only mention user feedback not B2B customer feedback:
* At Swype and Nuance
  * Feedback on Swype forums but overly focused on English  
  * Much more feedback once we had a direct-to-consumer offering on app stores, but rarely actionable
  * Infrequent public reviews
* At 98point6  
  * Some feedback on app stores, but it was rarely actionable
  * Some feedback in surveys which was more actionable
  * One time someone thanked me in person because our doctors might’ve saved their life
  * Some in-person feedback from doctors, who were also employees
* At S6
  * When we first opened access in Aug 2023, we immediately had more video of gameplay on Twitch than we could ever hope to review. If we’d been able to review it all maybe we could’ve had repro steps for thousands of bugs but it was just impossible
  * Drowning in feedback on Discord and Reddit. Discord was biased to be overly positive and Reddit was biased to be overly negative. Both were biased towards English feedback.
  * Once we launched on Steam, we were drowning in feedback from Steam reviews. Steam reviews also enabled more feedback outside of English.
  * There was enough culture around developer interactions that we had training for it.
  * Lots of feedback in surveys

I'm sometimes perplexed by the difference in feedback between 98point6 and Singularity 6. At 98point6 we saved our patients hours of frustration with the medical system and sometimes even saved their lives, yet the feedback was sparse. At Singularity 6 we provided entertainment and we were often drowning in complaints. At times I wondered: Are people more passionate about entertainment than life itself?

I came to think of it differently over the years, seeing it as:
- Feedback is dominated by the most passionate people. With a larger user base, you have more passionate people.
- I wonder if the passion is somewhat proporitional to the time investment. Someone might play Palia for 100 hours per year in constrast to using 98point6 for 30 minutes per year.
- In some ways feedback is relative to expectations. With healthcare, you're expected to save lives so it may not seem special even if it's valuable.

## TODO
- Approach the explanation as hypothesis testing: WHY are people so passionate
- Negative feedback at 98point6 was mostly some version of "I wanted antibiotics and the doctor didn't give them to me" in cases that were not bacterial

## See also
- Google UXR on positive vs negative experiences 1:3

# TO CONSIDER / TODO
- Consider alpha/beta testing
- Terminology: Studio, producer, game designer
- Timeline
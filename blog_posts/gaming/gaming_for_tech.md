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

TODO
- This needs a lot more writing and clarity
- * **“Some of that chaos is unavoidable… it’s part of building a creative work for entertainment.”**
- * Contrast *search* (finding fun) vs *optimize* (SaaS). Show two mini-stories: one where ambiguity produced a great feature; one where avoidable chaos cost a week.
* “The ‘fun’ (timed events) caused the scaling challenge. That’s innovation tax.”
















# Tooling

* “Unreal feels like Android Studio—powerful, less polished.”
* “Perforce is like git+DVC—but less polished in day-to-day ergonomics.”

# Dogfooding

* “Swype was easy to dogfood; everyone typed daily. Palia needed synchronized play windows. At 98point6, builders weren’t doctors.”

* “Fifty colleagues won’t surface what 500k players will.”

* Table: *Dogfoodability* across Keyboard App / Healthcare / MMO (what you learn vs what you miss).

* At 98point6 the software engineers weren’t doctors so we could only test the doctor experience so well. It also wasn’t a fun experience so people wouldn’t dogfood so much.  
* Dogfooding was pervasive at Swype where people would just load the newest build on their phones and use it daily. However, that dogfooding was biased towards English testing on top-end devices.  
* Dogfooding at S6 needed to be coordinated because many aspects of the game needed multiple people to test it. That dogfooding was generally biased towards top-end devices and good network conditions.

# FTUE

* “Onboarding in most apps is straightforward. Games are different—you’re teaching a new grammar.”

* “Tutorial popups are forgettable; quests that *force* you to learn are sticky.”

* “The best FTUE is invisible: you feel like you’re playing, not reading a manual.”

Similar to tech:
- Our onboarding at 98point6

Different than tech:
- There's often more to teach in gaming, because you often need to create a novel experience


# Distribution

* “Steam felt comparable to iOS/Android publishing. Nintendo/Xbox/Sony felt very different.”
* “Console launches bring reach but introduce certification rhythms and constraints.”  
  * *I’d love to write a bit about my stance on how deployment cadence determines the optimal amount of upfront planning vs iteration*
* Supposedly Apple’s app store was inspired by Nintendo (the percentage cut as well as the certification process). Otherwise pretty similar. Each platform has their own SDKs and APIs that you need to support. Each has their own cert process and requirements. Each takes a percentage cut of revenue.  
* Getting each update recertified drives your release cadence. If it takes a week for them to review an update, you can’t effectively pipeline weekly releases. So that pushes back the schedule. But then it’s tough so say 2 weeks of development on version 12 then 1 week of internal QA then 1 week of partner cert before launch. The dev team needs to move on to working on version 13 but by the time issues are raised in version 12 you might’ve forgotten about that implementation or not even have that code anymore.  
* Cross-platform is a similar challenge to the tech scene. Each platform has different requirements and you’re trying to minimize the amount of platform-specific work you do, but that’s not entirely possible.  
* Things like DORA metrics in tech are a bit limiting here.. You really can’t ship daily  
* Semi-decoupled backend APIs though, which added some risk

# Business stuff

* “There are thousands of good games; switching costs are near zero.”
* “A major genre-adjacent release can eclipse your update overnight.”
* Even more extreme than DTC. Say at Swype with DTC we had to work hard to earn a dollar or two. But there wasn’t as much competition. Gaming has tons of alternatives, and we’re competing for even less per player

# Operations

* “Healthcare chases 99.95% uptime; our game had planned downtime. That’s not negligence—it’s the cadence.”
* “Unreal forced client+server lockstep; old clients couldn’t hit new servers.”
* The deliberate scheduled deployment was something I took to heart in the tech world after seeing it in MMOs. Although I didn’t do scheduled deployments, we did deployment windows to ensure that we minimized risk (low CCU) and minimized reaction time (during work hours, not on Fridays)  
* When it’s handled well, in gaming players know when deployments happen and plan accordingly. They didn’t expect to log in on Tuesday at 10am so they generally aren’t mad about the game being down then. In contrast, unscheduled outages were much more disruptive. And similarly, if the downtime took much longer than expected players would be frustrated by that. For some of them, that day might be the only day they have free time and they were looking forward to relaxing but couldn’t. It’s important to see it from their view. Providing timely status updates helps a bit with that, though some issues really need to be prevented via better quality software practices (whether fewer manual steps, things that fail safely, more testing, etc)
* “Monthly trains felt normal in games; in healthcare we aimed for near-continuous delivery.”
* “Bigger windows tempt last-minute crams; you need guardrails.”

# Feedback

* “At 98point6 we were starved for unsolicited feedback; in games we were drowning in it.”
* “Fixes remove complaints; they rarely generate praise.”
* “Some devs disengaged after being dogpiled; training helped. CMs are shock absorbers.”
* “Bandwagon effects are real; narratives harden in public.”
* At S6  
  * When we first opened access in Aug 2023, we immediately had more video of gameplay on Twitch than we could ever hope to review. If we’d been able to review it all maybe we could’ve had repro steps for thousands of bugs but it was just impossible  
  * Discord/Reddit tons of people engaged. Each source of feedback had its own bias  
  * There was enough culture around dev interactions that we had to do training for it  
* At 98point6  
  * Very little specific feedback, mostly a star rating and a couple sentences at best.  
  * One time someone thanked me in person because our doctors might’ve saved their life.  
* At Swype  
  * Scattered feedback on forums but overly focused on English  
  * Had more volume of feedback once we were on app stores but with less depth
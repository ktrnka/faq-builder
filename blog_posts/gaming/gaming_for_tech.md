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
- Things I didn't experience personally

# Crunch mode and Chaos

The gaming industry has a reputation for crunch mode: If a team is behind schedule and headed towards a deadline, people often work longer hours to try and meet their target. In many companies it happens by mandate from leadership, in other cases it happens from pressure, and other crunch is opt-in, often by passionate developers.

My impression from S6 is that and the Doublefine documentaries is that:
1. It's popular to say "we don't crunch": The older generation of devs seem to say "never again" to the horrible crunch experiences they had
2. Crunching is less extreme than it was 20 years ago (but newer devs didn't experience the old crunch)
3. Companies are trying to do better for employees but progress is slow

Also note that crunch isn't fairly distributed. QA might be the last step and they're pushed to crunch. Or junior engineers may be more susceptible to leadership pressure. Or people in key, understaffed roles may come under more pressure.

The question I've pondered the most is: Why do gaming companies seem to crunch more than tech companies, and is it avoidable?

This is what I've observed: 
- Some chaos is avoidable
- Some chaos is unavoidable
- Crunching is a response to chaos, but not the only possible response

Let me give a few examples of avoidable chaos first, picking real examples that should be familiar to folks in tech:
- The work plan was unrealistic from the moment it was created
- Someone interpreted a Slack message or offhand comment from leadership as an urgent command
- The game would support PC and Nintendo Switch, but the design requirements of Switch were not taken into account during initial development
- The game was intentially designed to not be latency-sensitive, but a latency-sensitive feature was later added

I picked examples of communication issues because they're so common. In many of these cases, there wasn't enough communication or there was miscommunication. Another common theme is a refusal to prioritize, which is often a combination of communication and leadership problems.

Let me also give a few examples of unavoidable chaos. I'll start with one that's familiar in the tech industry: The team is working and runs into a surprise that needs to be addressed. That could be something as simple as learning that the plan will take much longer than expected, requiring adjustments to the schedule or plan. That's not to say that all surprises are unavoidable, many are, it's to say that all plans are vulnerable to unknown unknowns.

The unknowns can be much more fundamental. When you launch either a game or a product, you can't possibly anticipate everything so you're certain to face surprises at launch. An example from Palia was that we had many more players in Europe than expected so we added a European datacenter much sooner than planned, which took significant effort.

A different challenge is when you develop a game or level only to find that it isn't fun. The same happens in tech when we build a new product or feature only to find minimal engagement. In gaming we'd talk about "finding the fun" and in tech we talk about finding "product-market fit". It's slightly different because in the tech industry we're often solving a user need and there are many processes for translating user needs into potential solutions. In gaming, we sometimes have user needs but it's often a less specific user need. There are some processes to deliver consistent entertainment, but keep in mind that the same gameplay repeated over and over will often lose its entertainment value.

In the context of unavoidable chaos, "finding the fun" can take an unknown amount of time. If it takes much longer than expected and the game development has a fixed budget, it can eat into the time to make the game polished and clean.

## Takeaways
- There are similarities between creating a new game and creating new products, but it's a bit harder to find the fun compared to finding product-market fit
- Chaos can be lessened in well-run companies, but there's always going to be some of it

# Internal use aka Dogfooding

Dogfooding is an interesting topic across products and companies:

At Swype, developers could easily load builds on their personal phones. And because we were using our phones so much, we could quickly find out if a new build was an improvement or had some rare bug. Keep in mind that our developers mainly spoke English, so we didn't catch as many bugs in other languages.

At 98point6, our software enabled an online visit between a doctor and patient. That was much harder to dogfood so people dogfooded far less (perhaps 1% of the amount I saw at Swype). Exploratory dogfooding was more reserved for dedicated times when we had multiple people available and had an area of the product we wanted to focus on. Even still, we weren't doctors so our dogfooding of the clinical software wasn't as useful as our dogfooding of the patient software.

At Singularity 6, dogfooding (aka playtesting) needed to be coordinated because it was a multiplayer online game. So we had scheduled weekly playtests for the whole company. Sometimes those playtests had particular themes like a new event, and other times they were less structured. I'd say the amount of playtesting at S6 was comparable to Swype despite some of the difficulty of loading builds because of the cultural emphasis on dedicated playtesting time.

## Themes across companies
- Professionals tend to have high-end devices with good internet, and that's often unrealistic. Therefore we would discover fewer bugs affecting old devices or unreliable internet service
- Dogfooding is effective BUT has limitations for underrepresented groups (e.g., non-English, advanced users). And when I say "underrepresented" I mean underrepresented amongst the developers

## On ease of dogfooding / playtesting:
- S6: Internal Steam builds were by far the easiest to work with. The worst was when we got last-minute builds that took an hour to download. Switch and consoles were much tougher to dogfood as well, so they were playtested less
- Swype: It was easy to test Android builds due to sideloading, but much harder to test iOS builds

## Takeaways and opinions
- Ease of dogfooding has a major effect on bug discovery
- Dogfooding is a valuable process in building high quality software, but it has limitations to work around

And just to be clear here, I'm not suggesting that dogfooding is an alternative to actual testing. It's complementary to many forms of testing and a key part of your suite of quality-improvement efforts. Beyond that, it's also a helpful effort to keep everyone in the company aligned with the user's experience.

# Distribution

Selling a game on Steam is comparable to publishing an Android app on Google Play. Both platforms take a 30% cut of revenue, have some requirements about what you can publish, and provide some some software libraries or services. In both cases you need to optimize your app for the store to make it more discoverable and drive growth.

Publishing an app on the iOS App Store is a bit more burdensome due to the manual review process. That can be good for quality and consistency, but the review process can also be inconsistent. We had some frustrating times at 98point6 when a bug fix was blocked because the App Store reviewer was flagging something from a prior version. That introduced delays and sometimes degraded the user's experience.

In the gaming world, publishing for Nintendo Switch is somewhat similar. They have a certification process similar in spirit to the iOS process, but it was a little slower and more involved. Also the certifcation rules required an NDA to access, which added another challenge.

Multi-platform distribution is very similar between gaming and non-gaming software:
- You're juggling the competing requirements of each platform and trying to minimize platform-specific work, while recognizing that the importance of some platform-specific work (e.g., consistency of game controls on Switch or consistency of UI across iOS apps)
- You're trying to design a release cadence to balance the constraints of all platforms and that often is determined by the slowest platform to release on
- Backend APIs allow more flexibility in release cadence, but they require extra care to test and update without client updates. I found this was often much easier in tech than gaming

## Takeaways
- Distribution heavily influences release process optimization including the cadence of releases
- Discussion of "what goes in the client vs backend" should really consider release cadence more than it does

Things I prefer from mobile app distribution
- The requirements are usually more clear, and most of them are publicly available
- The certification process is pretty fast

Things I prefer from gaming distribution
- Steam provides much more value-add in the form of APIs and discoverability compared to app stores

Things I wish were changed
- I wish cert requirements were public for all platforms (Xbox is good about this)
- I wish all requirements also included the intention not just the rule

# Business

If someone doesn't like your game, they can easily find something better to do with their time. For one, they can easily find another game to try. The switching cost is nearly zero. If you have a free-to-play game, players are even quicker to drop your game.

Gaming is tougher than I've described so far:
- You might plan your game launch only to be eclipsed by a hit game launching around the same time
- You're not just competing against new releases but also competing against decades of amazing games
- You're not just competing against the same type of game, but many types of games
- For some players, you're also competing against other forms of entertainment not just gaming

## Takeaways
- I have a lot more respect now for developers that succeed financially
- B2B/SaaS companies tend to provide far more stability than I previously appreciated

# Operations

I found it interesting to compare and contrast the operations of 98point6 (24/7 healthcare) to Palia (24/7 gaming). 

At 98point6 we emphasized reliability and scrutinized our service availability. Some years we delivered 99.9%, others closer to 99%. For reference, 99.9% availability means about 9 hours of downtime per year whether planned or unplanned. That's just one or two bad outages per year.

In online gaming it's common to have scheduled downtime. That's a time when the game client may be updated, servers may be updated/restarted, and so on. When things went really well, that would only take 1-2 hours per week (~99% uptime). Coming from healthcare initially I scoffed a bit at the downtime but our tech stack didn't allow much choice but to bring the game down for updates. That said I'm sure we could've done better, whether more thorough testing, use of feature flags, etc.

The difference in scale was neat too: At 98point6 we wanted 99.9% uptime for about 100-1,000 daily active users. At Singularity 6 I wanted 99% uptime for about 100,000-1,000,000 daily active users.

After seeing both in practice, I thought less about availability as a percentage of time and more about broken user expectations. For example, in Palia our players expected downtime on Tuesday mornings and planned accordingly. It didn't bother most people. 

What bothered players was unexpected downtime and unexpected instability. Like when the 2 hour downtime turned into 6 hours. Or some players may not expect instability after major updates.

# User feedback

First let me just mention the type and scale of feedback across former employers:
* At Swype and Nuance
  * A tiny number of bloggers and news sites would provide detailed feedback
  * A small number of users commented on our forums, but overly biased towards English  
  * A large number of users gave app store reviews, but the reviews were rarely actionable
* At 98point6  
  * Some patients provided feedback on app stores, but like Swype it was rarely actionable
  * A smaller number of patients responded to our surveys with much more actionable feedback
  * One time someone thanked me in person because our doctors might’ve saved their life
  * Our doctors (also a part of the business) would provide feedback in person or in Slack
* At S6
  * When we first opened access in Aug 2023, we immediately had more hours of recorded gameplay on Twitch than we could ever hope to review. If we’d been able to review it all maybe we could’ve had repro steps for thousands of bugs but it was just impossible (note: someone please make a startup to create/update bug reports from Twitch)
  * We were consistently drowning in feedback on Discord and Reddit. Discord was biased to be overly positive and Reddit was biased to be overly negative. Both were biased towards English feedback.
  * Once we launched on Steam, we were drowning in feedback from Steam reviews. Steam reviews also enabled more feedback outside of English.
  * There was enough culture around developer interactions that we had formal training for it.
  * Many players responded to surveys as well.

I'm sometimes perplexed by the difference in feedback between 98point6 and Singularity 6. At 98point6 we saved our patients hours of frustration with the medical system, hundreds of dollars, and sometimes even saved their lives, yet the feedback was sparse. At Singularity 6 wse provided entertainment and we were drowning in feedback. At times I wondered: Are people more passionate about entertainment than life itself?

I came to think of it differently over the years, seeing it as:
- With a larger user base, you have more passionate people and my time with feedback is sometimes taken over by the most passionate users
- Passion is somewhat proporitional to the time investment. Someone might play Palia for 100 hours per year in constrast to using 98point6 for 30 minutes per year.
- Feedback is relative to expectations. With healthcare, you're expected to save lives so it may not seem special even if it's very valuable. Sometimes those expectations are also unrealistic, like when patients expected antibiotics for viral infections.

## See also
- Google UXR on positive vs negative experiences 1:3

# TO CONSIDER / TODO
- Consider alpha/beta testing
- Terminology: Studio, producer, game designer
- Timeline

# Honorable mentions

I found these differences interesting, but don't have much to say about them. I'm only briefly mentioning them to provide some areas that might be worth searching for:

- Developing in Unreal felt a lot like developing in Android Studio in terms of many aspects of the IDEs. I just wish that blueprints had a text version to diff in version control like Android layout files. It was frustrating to ask for review of a bunch of screenshots, especially for Blueprints that were large.
- Perforce was frustrating in many ways, but we couldn't "just use git" due to lots of large binary files. That was familiar to my experiences in versioning ML models.
- The onboarding experience in gaming is often called FTUE (first-time user experience). There's a significant amount of effort put into that because games often have complex rules and mechanics to explain. Players aren't going to read manuals much so you need to incrementally teach them the rules in ways that are fun.

# See also

- The Palia software page

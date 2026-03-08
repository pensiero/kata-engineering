I want to brainstorm with you how we can update the AGENTS.md file and use/create skills file to improve the way we build software projects.

I explain you the problem.
After working with AI agents like you for a while on a project, I realize that:
- you add a lot of complexity and I need to often review it, simplify and reinforce boundaries
- you tend to lose the point of what we are building
- fragility is added to random places
- it's harder to spot bugs because they get hidden across a bigger codebase which apparently just looks fine
- if I give you once the instruction of building tests, enforce schemas, use invariants - you may use couple of times, but with the time you forget to use them regularly
- you tend to get stuck with the same idea and it's difficult to let you explore alternatives - when you start you are much more keen to try different approaches. this leads to stagnation
- I need to specify for every project basic architectural guidelines I want you to follow, and you end up not following them consistently with the time

One possible option I thought is to leverage multiple specialized agents, use skills and tweak properly the AGENTS.md file.

This company is trying an interesting and novel approach: https://every.to/guides/compound-engineering <- read this carefully, notions inside can be helpful for what I want to achieve. Here https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering you find all the instructions given to the various agents. Look at each file in that repo very carefully, especially at agents docs (https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering/agents), as they can help in achieving the goal here.
They are using multiple specialized agents, and seems they defined well boundaries, standards and best practices. 

Given the agentic AI technology is evolving so fast, every week something new, I want to build something simple. The more complicate the wrapper, the more unuseful and outdated will become in 2/3 months. So I thought starting simple, with just 2 agents, a coder/architect and a reviewer. I'm not sure if I should just tweak their AGENTS.md file, or if I should rather use skills, or a mix. I need your opinion, and it must not be biased by my reasonings. 

It's also interesting to read Claude team's idea around best practices when using Claude agents https://code.claude.com/docs/en/best-practices and best practices on skills authoring: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices . Use them to accomplish what we want to accomplish here, if you think they are helpful.

This user also explained here a lot that you should take in consideration to achieve what I'm trying to achieve here: https://x.com/systematicls/status/2028814227004395561 <-- read it carefully, and take information from here. I'm very aligned with ideas and concepts explained in that post.

You can find some approaches of skills inside your workspaces, under the "skills" folder (/Users/oscar/.openclaw/workspace/skills). the "architect-old" skill was the first trial, and was encompassing a lot of things. Then I tried to simplify and split into architect and coder skills, but I realized having 2 agents for doing such things is a lot of back and fort without a framework around it. And probably overkilling for personal projects, the ones I'm mostly building at this stage. Please read all the skills so you understand my intent. Again, those skills are probably not well written, structured and the content may not be what I'm looking for, but you understand the intent, and partially what I'm aiming for.

Also check out the project engram, sitting at /Users/oscar/Projects/engram. Check the structure, architecture of project, compositions, documentation, tests, etc. It doesn't matter what the project is about - look how I structured it. Which best practices I asked agents to follow while building it, like writing schemas, fixtures, tests, invariants. By using an ARCHITECTURE, IMPLEMENTATION and contracts documents. Those are just example. I built that with an agent, after many iterations, so represents a bit where my head is heading, but I believe can be improved by giving agents clear guardrails and directives that are respected at every prompt. 

At the same time, I don't want paralize the agents with too strict directives. Freedom of exploration, trying alternatives is critically important.

The approach I'd like to build is standards, best practices and guardrails that should help anyone new to the codebase to just keep working from where I left. Even if the person doesn't know what kind of ideas I have to structure the projects, this person's agent should have clear instructions and guardrails to understand how the project took the shape that it actually took. Surely a lot can be reverse engineered by the agent by looking thoroughly all the files, but the final result might not be perfect, and the agent must rediscover everything by itself at each new session, which I don't find efficient.

Let's brainstorm together before going into action mode.

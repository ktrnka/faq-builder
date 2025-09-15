# Planning step 1: Identify a grouping of sources

This step should identify potential sources by reviewing `reddit_classifications.md` and `youtube_classifications.md` for coherent topic clusters.

**Initial Source Discovery:**
- Target 3-7 sources covering related topics
- Note target audience from audience tags in classifications  
- See `categorization_manual.md` for grouping guidance
- **Start broad**: Include potentially relevant sources even if unsure

**Content Density Check:**
- Estimate content richness from classification summaries
- Look for sources with detailed Keith responses vs brief mentions
- Consider whether grouping provides enough material for substantial blog post

**Experience Alignment:**
- Prioritize topics where Keith has direct industry experience
- Flag areas where expertise may be limited
- Consider whether personal experience stories could supplement technical content

# Planning step 2: Fetch the verbatim content

This step fetches cleaned content from each source using CLI commands:
- `uv run faq-builder reddit show-thread POST_ID_OR_FILE`
- `uv run faq-builder youtube show-cleaned-transcript video_id_or_file`

**Content Assessment:**
- Include date and permalink to original sources
- **Evaluate richness**: Does each source provide substantial, detailed content?
- **Check expertise alignment**: Which topics have Keith's direct experience vs general knowledge?
- **Note content gaps**: Are there thin areas that need additional sources?

**Iteration Decision Point:**
- If content feels thin: search for additional sources before proceeding
- If some sources are weak: consider removing them to focus on stronger content
- If expertise gaps exist: decide whether to find supplementary sources or narrow scope

# Planning step 3: Rough outline the blog post

Create overview and rough outline identifying main points and supporting sources.

**Blog Structure:**
- Write compelling title that captures unique angle or insight
- Create overview positioning the topic (why it matters, what's unique about the perspective)
- Map main points to supporting sources
- **Add meta-insights**: Connect individual topics to broader domain patterns or challenges

**Context Assessment:**
- Include important context from original questions/discussions (non-Keith perspectives)  
- Identify missing context that would help readers understand the "why"
- **Consider broader implications**: How do these specific examples illustrate larger principles?

**Unique Value Identification:**
- What makes this perspective different from generic content on the topic?
- Which insights come from direct experience vs general knowledge?
- How does Keith's cross-domain experience (gaming + ML + consulting) provide unique angles?

# Planning step 4: Re-review and enhance

**Gap Analysis:**
- Re-review classifications for missed closely-related sources
- **Active search**: Use grep/semantic search if content feels thin
- Consider whether additional domains could strengthen the narrative

**Content Enhancement:**
- **Meta-synthesis**: Connect themes across sources to identify broader patterns
- **Domain insights**: Add sections explaining why the domain has these challenges
- **Experience prioritization**: Emphasize areas with strongest direct experience

**Quality Assessment:**
- Does the plan provide enough substantial content for target length?
- Are insights actionable and specific rather than generic?
- Would the target audience find this valuable enough to share/reference?

**Scope Refinement:**
- Remove or de-emphasize areas with limited expertise
- Focus on strongest content and insights
- **Plan for constraints**: Note which sections could be cut if time/length becomes limiting

**Template Meta-Learning:**
- What worked well in this planning process?
- What gaps or friction points emerged?
- How could future planning be more efficient or effective?

---

**Note**: Expect significant iteration on both this template and planning docs. Early attempts will help refine the approach for future blog planning. The goal is to develop a reliable process for creating substantial, valuable content that leverages Keith's unique cross-domain expertise.
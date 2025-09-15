# Planning step 1: Identify a grouping of sources

This step should simply list the data sources in a format that makes them easy to look up. This can be built by reviewing `reddit_classifications.md` and `youtube_classifications.md` to identify which posts/chapters belong to the same topic cluster.

Target a coherent grouping of 2-7 sources that cover common topics. See `categorization_manual.md` for additional guidance on what makes a good grouping. Note the target audience from the audience tags in the classifications.

# Planning step 2: Fetch the verbatim content

This step should run the appropriate `uv run faq-builder ...` commands to fetch the cleaned content from each source:
- `uv run faq-builder reddit show-thread POST_ID_OR_FILE`
- `uv run faq-builder youtube show-cleaned-transcript CLEANED_FILE`

The classifications don't always have enough information to get the filenames, so you may need to look up the actual filenames in `data/reddit/threads/` and `data/youtube/cleaned/`.

When including the verbatim content, if possible include the date and a permalink to the original source.

# Planning step 3: Rough outline the blog post

This step should create a few sentence overview, then a rough outline identifying the main points and which sources support each point. The goal is to fill in the planning template structure rather than write the actual blog post.

In this section we should also identify:
- Any important context from the original question or discussion that isn't from me
- Any missing context that would help the readers better understand the "why" behind the topic

# Planning step 4: Re-review sources for missing content

This step should re-review the sources from step 1 to see if we missed any closely related sources, and add them. It should also critique what we've planned so far to identify improvements.

Note: We expect to iterate on this template and these planning docs significantly as we try this process a few times. The early attempts will help us refine the approach for future blog post planning.
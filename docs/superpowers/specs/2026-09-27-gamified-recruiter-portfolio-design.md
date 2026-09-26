# Gamified Recruiter Portfolio Design

## Purpose

Create a standalone one-page portfolio for Ishaan Chandak at `https://ishaan-chandak.github.io`. The site must help a recruiter quickly understand who Ishaan is, what he has built, the impact of his work, and how to contact him. It should preserve the game-inspired identity of his GitHub profile without making information harder to find.

Success means a recruiter can identify Ishaan's current role, strongest engineering evidence, core technical range, and contact options in roughly one minute.

## Audience and Positioning

The primary audience is technical recruiters and hiring managers considering Ishaan for software engineering roles. The site should position him as a software engineer who builds reliable services, data workflows, and thoughtful automation.

The experience must feel professional first and game-inspired second. Familiar portfolio labels remain visible, while secondary game terminology adds personality:

| Standard label | Game treatment |
| --- | --- |
| Hero | Player Spawn / Current Mission |
| About | Player Lore |
| Experience | Campaign History |
| Projects | Boss Battles / Mission Debriefs |
| Technical toolkit | Loadout / Equipment Vault |
| GitHub activity | Live Telemetry |
| Contact | Open Comms |

## Visual Direction

Use the approved **Recruiter HUD** direction:

- Dark teal command-deck palette with restrained warm-gold emphasis.
- Subtle grid texture and fine borders instead of dense decoration.
- Editorial sans-serif typography for primary content, with monospace type for labels and telemetry.
- Generous spacing and a clear reading hierarchy inspired by elegant editorial portfolios.
- Gold is reserved for meaningful actions, section markers, and evidence inside work descriptions.
- Game styling appears through terminology, small status indicators, progress details, and interface framing—not oversized score counters.

The hero must remain quiet and focused. It contains Ishaan's name and role, a concise positioning statement, his current Goldman Sachs role, and primary actions for viewing work, downloading the resume, or making contact. It must not contain a row of loud metrics.

## Information Architecture

The page is a single scrolling experience with the following order:

1. **Hero and current mission** — identity, positioning, current Goldman Sachs role, resume, and contact actions.
2. **About** — a concise introduction to Ishaan's engineering mindset, preferred problems, and growth direction.
3. **Experience** — the full current Goldman Sachs role followed by progressively shorter entries for Goldman Sachs Summer Analyst, Techligence, and Indian Oil.
4. **Selected projects** — Mango Attribute Detection and DermAI presented as engineering case studies.
5. **Technical toolkit** — technologies grouped by purpose rather than presented as an undifferentiated logo wall.
6. **Education** — VJTI, B.Tech Information Technology, 9.00/10 CGPA, relevant coursework, and certifications.
7. **Achievements, leadership, and community** — AIR 9, MHT-CET rank, Pratibimb, Community of Coders, the Healing Fields proposal, and Community TeamWorks.
8. **GitHub activity and links** — one restrained contribution visualization plus GitHub, LinkedIn, and resume links. Existing profile widgets should not be duplicated into a noisy dashboard.
9. **Contact** — a short invitation to connect through professional email or LinkedIn.

The recruiter journey is identity → evidence of work → technical depth → credentials → contact.

## Content Design

### Experience

Each substantial role includes:

- A short statement describing responsibility and scope.
- Two to four achievement points covering the problem, contribution, technology, and outcome.
- A quiet row of relevant technologies.
- Quantified evidence emphasized within the sentence that explains it.

The current Goldman Sachs role receives the most detail. It covers:

- Java and Quarkus microservices connecting internal engines with Microsoft Power Platform and Teams workflows.
- The AWS ETL workflow using S3, Lambda, Glue, EventBridge, SQS, and Aurora to ingest more than 15 operational datasets into Celonis.
- Privacy and access controls using Presidio, IAM, and KMS, with no sensitive PII exposed through the pipeline.
- Cross-functional architecture, failure handling, and production reliability work.

The Goldman Sachs Summer Analyst entry explains the Go reporting pipeline, removal of manual reporting effort, and the 40% reduction in operational overhead. Techligence and Indian Oil remain concise while retaining their clearest contributions and results.

Metrics must never appear as decorative scores. They are evidence embedded in the relevant narrative.

### Projects

Each selected project is a compact case study with:

- The problem and why it mattered.
- Ishaan's role and contribution.
- The technical approach.
- A measurable or observable result.
- Links to code or a demonstration when a reliable public link exists.

Mango Attribute Detection is the flagship project and includes Ishaan's team-lead role, the annotated dataset, model stack, and 13.37% accuracy improvement. DermAI is presented as a secondary applied-ML project.

### Technical Toolkit

Group technologies into purposeful categories such as backend and systems, data and machine learning, frontend, cloud, and developer tooling. This section supports the experience and project evidence; it does not replace it.

## Interaction Design

- Use a slim sticky navigation that highlights the current section.
- Show a subtle mission-progress line based on page position.
- Reveal content gently as it enters the viewport.
- Allow experience and project cards to lift slightly on hover.
- Add a restrained pointer-reactive glow in the hero, without replacing the native cursor.
- Keep project evidence visible in the page. Do not hide essential information in modals, accordions, or game unlocks.
- Do not use a loading screen, background music, particle storm, forced tutorial, or interaction that blocks normal scrolling.

All interactions must be enhancements. The complete content remains readable when JavaScript or animation is unavailable.

## Responsive and Accessible Behavior

- Preserve the content order on desktop, tablet, and mobile.
- Collapse multi-column layouts into one column on small screens.
- Remove or simplify nonessential decoration where it competes with mobile readability.
- Use semantic landmarks and headings, keyboard-operable navigation, visible focus states, useful link text, and sufficient contrast.
- Honor `prefers-reduced-motion` by disabling pointer effects, scroll reveals, and nonessential transitions.
- Avoid a custom cursor and interactions that depend exclusively on hover.

## Technical Architecture

Create a dedicated GitHub repository named `Ishaan-Chandak.github.io`. Use Astro to generate static HTML, CSS, and minimal client-side JavaScript.

Separate portfolio content from presentation components so resume updates do not require rewriting layouts. The main units are:

- A structured content module for profile, experience, projects, education, achievements, links, and contact data.
- Focused page-section components with clear content inputs.
- Small, isolated client scripts for active-section navigation, page progress, scroll reveals, and the optional hero glow.
- Shared design tokens and responsive styles.
- A local public resume PDF used by the download action.

No database, API server, contact backend, analytics service, or large animation library is required for the first version.

GitHub Actions builds and deploys the production site whenever the main branch changes. The production base URL is `https://ishaan-chandak.github.io`.

## Privacy and Content Integrity

- Do not publish Ishaan's phone number or home address.
- Publish only the professional email address, GitHub profile, LinkedIn profile, and approved resume download.
- Keep all claims faithful to the provided resume source.
- Do not invent metrics, technologies, project links, or role responsibilities.
- If a public project URL is unavailable, omit the link rather than rendering a broken or placeholder action.

## Failure Handling

The site is static and must remain useful if optional enhancements fail:

- Content renders as HTML before client scripts run.
- Navigation anchors work without JavaScript.
- Missing optional external links cause the associated action to be omitted.
- The resume is stored locally so downloading does not depend on Google Drive availability.
- Decorative assets have CSS or text fallbacks and never carry essential information.
- Deployment must fail visibly if the production build fails.

## Verification

Before deployment, verify:

- The production build succeeds without warnings that affect functionality.
- Every section appears in the approved order with accurate resume content.
- All internal anchors, external links, and the resume download work.
- Desktop and mobile layouts preserve hierarchy and do not overflow.
- Keyboard navigation, focus visibility, heading structure, color contrast, and reduced-motion behavior meet the stated accessibility rules.
- The page remains readable with JavaScript disabled.
- No private phone number or home address appears in generated files.
- Production deployment serves the site at the intended GitHub Pages URL.

## Out of Scope for Version One

- A CMS or admin panel.
- A contact form backend.
- Visitor accounts, saved state, or game progression.
- Audio, music, heavy particle systems, or 3D scenes.
- A blog engine.
- Live data integrations beyond a restrained GitHub contribution visualization.
- Publication of private contact details.

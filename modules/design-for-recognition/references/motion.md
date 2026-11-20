# Motion and temporal design

Design movement as part of what happens after a person acts or the system changes state. Give frequent actions immediate acknowledgement and a brief transition when it helps someone follow the change. Reserve richer movement for moments where the context or product's character warrants it.

## Specify the transition

For each meaningful transition, describe the trigger, starting and resulting states, and what the person should understand. Identify the visual relationship to preserve, which element leads, and where a surface appears to come from. A disclosure can enter from its trigger. A queue can retain the follow-up's text and position as its status changes from waiting to held. Use visible labels and accessible feedback to communicate state in every motion preference. Show progress only at the precision the system can support.

Choose duration and easing for how often the action occurs, its travel or scale, and the pace needed to follow it. Let pressed and frequent controls respond immediately. Use easing for clear acceleration and settling, and consider springs for movement that follows a gesture, changes direction, or needs momentum. Stage related movements around the main change. Use existing motion tokens or name reusable durations and easing by role when multiple transitions share them.

## Keep actions available through change

Set the real state and update focus, status, and input availability as the action happens. Give dismissal, reversal, and repeated input a coherent path from the current state. Cancel stale effects when a newer action replaces them. Define a reduced-motion treatment that preserves the same content, hierarchy, controls, and feedback with immediate updates or a restrained alternative. For web work, respect `prefers-reduced-motion` and use properties such as `transform` and `opacity` where they express the transition efficiently. Measure rendering when movement or responsiveness is part of the design question.

Replay the transition with ordinary and reduced-motion settings. Interrupt or reverse it while movement is still in progress and check that the latest action determines the final state. Inspect the interaction in the contexts that affect it, such as keyboard, touch, or a constrained device. Check that the static outcome conveys the same meaning and usable recovery as the animated one.

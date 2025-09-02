### Summary

**Key takeaways**

- Typical period data use (monthly subscriptions only; 96% of all subscriptions): **8,043** subscriptions; **median 139 MB**; **mean 1.4 GB**; **IQR 9–533 MB**.
- By plan data allowance (monthly subscriptions only):
  - **0 GB**: 4 subscriptions; median **337 MB**; mean **10.7 GB**; IQR **0–11.1 GB**.
  - **1 GB**: 5,805 subscriptions; median **118 MB**; mean **370 MB**; IQR **6–358 MB**. **Average utilization: 37%.**
  - **5 GB**: 887 subscriptions; median **392 MB**; mean **1.75 GB**; IQR **25 MB–2.5 GB**. **Average utilization: 35%.**
  - **Unlimited**: 1,722 subscriptions; median **2.2 GB**; mean **10.1 GB**; IQR **72 MB–10.8 GB**.
  - **Observation:** 1 GB and 5 GB plans show low utilization. 0 GB and Unlimited plans both exhibit a long tail of heavy users.
  - **Data per dollar:** Unlimited Data users consumed **123 MB/\$**, Ultra Unlimited **763 MB/\$**, Easy Plan (1 GB) **12 MB/\$**. These are the plans with the highest amount data consumed and ordered in decreasing order.
- **Data usage is highly volatile.** Excluding subscriptions with only one reporting period. For each subscription, we compute each month's change relative to the previous month, and for **79% of subscriptions, the average of month-on-month changes exceeds 50%.**
- **Retention:** The latest project (**People Mobile**) underperforms older projects: **37% after 1 month**, **12% after 2 months**. The first project (**ACME Phone**) leads with **88% after 1 month**, **78% after 2 months**, and **55% after 6 months**.

**Recommendations**

1. For under-utilized plans, consider introducing an intermediate tier to better match demand and lift utilization.
2. For Unlimited plans, assess top-decile usage as a cost risk (p90 = 24 GB). Evaluate whether fair-use caps are appropriate; this will require cost data and clarity on company priorities.
3. People Mobile is the first API product for mobile phones. Investigate drivers of lower retention: compare user demographics, product features, and experience (e.g., onboarding, billing/renewal, notifications) against the two other projects. If comparability is limited, deep-dive into People Mobile user behaviour and run A/B tests to improve retention.
4. Conduct market analysis and A/B testing on plan design and consider expanding add-ons (e.g., hotspot, roaming bundles).

**Next steps / questions**

- Some subscriptions are very short (1–5 days). Understand why customers choose these products and explore targeted offerings for this segment.
- Some users do not use data in the first few months, we should investigate the causes and understand how this feeds into utilization and retention.
- Analyse retention across more dimensions (e.g., device/phone type, geography; plan details such as add-ons, network carrier; 1-month vs 30-day plans).
- Examine what happens when a plan is updated, the exisiting data does not show complete information.
- Understand the accounting logic that should applied when a subscription changes plan.

**Assumptions**

- **Subscription length.** Only subscriptions with periods between **28 and 31 days** are included (96% of all subscriptions). Shorter periods are filtered out to keep periods comparable. With daily-level data we could include these in statistical analysis.
- **Plan attributes over time.** This analysis uses the **current** plan state. A deeper cut should align the plan version to each reporting period. Relevant allowance attributes did not change across plan events; plan-validity metadata was not used.
- **Retention definition.** Retention is the share of original subscriptions that have a record at period *n*. This assumes `subscription_period_number` increments sequentially without gaps for active subscriptions. Subscriptions whose first observed period number is more than 1 (29 subscriptions in total) were excluded from the retention analysis.
- **Subsciprtion double counting.** 598 subscriptions have more than 1 plan. These subscriptions will be counted in both plans (or more if exists) when the metrics are grouped by plans.

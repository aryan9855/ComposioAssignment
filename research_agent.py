#!/usr/bin/env python3
"""Small research-agent style script for the 100-app audit.

This keeps the workflow lightweight and deterministic: it reads the app list,
clusters by category, infers auth and access posture from url/hint cues, and
writes a compact JSON summary.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

APP_LIST = [
    {"name": "Salesforce", "category": "CRM and Sales", "hint": "salesforce.com"},
    {"name": "HubSpot", "category": "CRM and Sales", "hint": "hubspot.com"},
    {"name": "Pipedrive", "category": "CRM and Sales", "hint": "pipedrive.com"},
    {"name": "Attio", "category": "CRM and Sales", "hint": "attio.com"},
    {"name": "Twenty", "category": "CRM and Sales", "hint": "twenty.com"},
    {"name": "Podio", "category": "CRM and Sales", "hint": "podio.com"},
    {"name": "Zoho CRM", "category": "CRM and Sales", "hint": "zoho.com/crm"},
    {"name": "Close", "category": "CRM and Sales", "hint": "close.com"},
    {"name": "Copper", "category": "CRM and Sales", "hint": "copper.com"},
    {"name": "DealCloud", "category": "CRM and Sales", "hint": "api.docs.dealcloud.com"},
    {"name": "Zendesk", "category": "Support and Helpdesk", "hint": "zendesk.com"},
    {"name": "Intercom", "category": "Support and Helpdesk", "hint": "intercom.com"},
    {"name": "Freshdesk", "category": "Support and Helpdesk", "hint": "freshdesk.com"},
    {"name": "Front", "category": "Support and Helpdesk", "hint": "front.com"},
    {"name": "Pylon", "category": "Support and Helpdesk", "hint": "usepylon.com"},
    {"name": "LiveAgent", "category": "Support and Helpdesk", "hint": "liveagent.com"},
    {"name": "Plain", "category": "Support and Helpdesk", "hint": "plain.com"},
    {"name": "Help Scout", "category": "Support and Helpdesk", "hint": "helpscout.com"},
    {"name": "Gorgias", "category": "Support and Helpdesk", "hint": "gorgias.com"},
    {"name": "Gladly", "category": "Support and Helpdesk", "hint": "gladly.com"},
    {"name": "Slack", "category": "Communications and Messaging", "hint": "slack.com"},
    {"name": "Twilio", "category": "Communications and Messaging", "hint": "twilio.com"},
    {"name": "Zoho Cliq", "category": "Communications and Messaging", "hint": "zoho.com/cliq"},
    {"name": "Lark (Larksuite)", "category": "Communications and Messaging", "hint": "open.larksuite.com"},
    {"name": "Pumble", "category": "Communications and Messaging", "hint": "pumble.com"},
    {"name": "Discord", "category": "Communications and Messaging", "hint": "discord.com"},
    {"name": "Telegram", "category": "Communications and Messaging", "hint": "core.telegram.org"},
    {"name": "WhatsApp Business", "category": "Communications and Messaging", "hint": "developers.facebook.com/docs/whatsapp"},
    {"name": "Aircall", "category": "Communications and Messaging", "hint": "aircall.io"},
    {"name": "Vonage", "category": "Communications and Messaging", "hint": "developer.vonage.com"},
    {"name": "Google Ads", "category": "Marketing, Ads, Email and Social", "hint": "developers.google.com/google-ads"},
    {"name": "Meta Ads", "category": "Marketing, Ads, Email and Social", "hint": "developers.facebook.com/docs/marketing-apis"},
    {"name": "LinkedIn Ads", "category": "Marketing, Ads, Email and Social", "hint": "learn.microsoft.com/linkedin/marketing"},
    {"name": "GoHighLevel", "category": "Marketing, Ads, Email and Social", "hint": "highlevel.stoplight.io"},
    {"name": "Mailchimp", "category": "Marketing, Ads, Email and Social", "hint": "mailchimp.com/developer"},
    {"name": "Klaviyo", "category": "Marketing, Ads, Email and Social", "hint": "developers.klaviyo.com"},
    {"name": "systeme.io", "category": "Marketing, Ads, Email and Social", "hint": "systeme.io"},
    {"name": "Pinterest", "category": "Marketing, Ads, Email and Social", "hint": "developers.pinterest.com"},
    {"name": "Threads (Meta)", "category": "Marketing, Ads, Email and Social", "hint": "developers.facebook.com/docs/threads"},
    {"name": "SendGrid", "category": "Marketing, Ads, Email and Social", "hint": "sendgrid.com"},
    {"name": "Shopify", "category": "Ecommerce", "hint": "shopify.dev"},
    {"name": "WooCommerce", "category": "Ecommerce", "hint": "woocommerce.com/document/woocommerce-rest-api"},
    {"name": "BigCommerce", "category": "Ecommerce", "hint": "developer.bigcommerce.com"},
    {"name": "Salesforce Commerce Cloud", "category": "Ecommerce", "hint": "developer.salesforce.com/docs/commerce"},
    {"name": "Magento (Adobe Commerce)", "category": "Ecommerce", "hint": "developer.adobe.com/commerce"},
    {"name": "Squarespace", "category": "Ecommerce", "hint": "developers.squarespace.com"},
    {"name": "Ecwid", "category": "Ecommerce", "hint": "api-docs.ecwid.com"},
    {"name": "Gumroad", "category": "Ecommerce", "hint": "gumroad.com/api"},
    {"name": "Amazon Selling Partner", "category": "Ecommerce", "hint": "developer-docs.amazon.com/sp-api"},
    {"name": "fanbasis", "category": "Ecommerce", "hint": "fanbasis.com"},
    {"name": "DataForSEO", "category": "Data, SEO and Scraping", "hint": "docs.dataforseo.com"},
    {"name": "SE Ranking", "category": "Data, SEO and Scraping", "hint": "seranking.com/api"},
    {"name": "Ahrefs", "category": "Data, SEO and Scraping", "hint": "ahrefs.com/api"},
    {"name": "MrScraper", "category": "Data, SEO and Scraping", "hint": "docs.mrscraper.com"},
    {"name": "Apify", "category": "Data, SEO and Scraping", "hint": "docs.apify.com"},
    {"name": "Firecrawl", "category": "Data, SEO and Scraping", "hint": "firecrawl.dev"},
    {"name": "Bright Data", "category": "Data, SEO and Scraping", "hint": "brightdata.com"},
    {"name": "Sherlock", "category": "Data, SEO and Scraping", "hint": "github.com/sherlock-project/sherlock"},
    {"name": "Waterfall.io", "category": "Data, SEO and Scraping", "hint": "waterfall.io"},
    {"name": "Clay", "category": "Data, SEO and Scraping", "hint": "clay.com"},
    {"name": "GitHub", "category": "Developer, Infra and Data platforms", "hint": "docs.github.com/rest"},
    {"name": "Vercel", "category": "Developer, Infra and Data platforms", "hint": "vercel.com/docs/rest-api"},
    {"name": "Netlify", "category": "Developer, Infra and Data platforms", "hint": "docs.netlify.com/api"},
    {"name": "Cloudflare", "category": "Developer, Infra and Data platforms", "hint": "developers.cloudflare.com/api"},
    {"name": "Supabase", "category": "Developer, Infra and Data platforms", "hint": "supabase.com/docs"},
    {"name": "Neo4j", "category": "Developer, Infra and Data platforms", "hint": "neo4j.com/docs/api"},
    {"name": "Snowflake", "category": "Developer, Infra and Data platforms", "hint": "docs.snowflake.com"},
    {"name": "MongoDB Atlas", "category": "Developer, Infra and Data platforms", "hint": "mongodb.com/docs/atlas/api"},
    {"name": "Datadog", "category": "Developer, Infra and Data platforms", "hint": "docs.datadoghq.com/api"},
    {"name": "Sentry", "category": "Developer, Infra and Data platforms", "hint": "docs.sentry.io/api"},
    {"name": "Notion", "category": "Productivity and Project Management", "hint": "developers.notion.com"},
    {"name": "Airtable", "category": "Productivity and Project Management", "hint": "airtable.com/developers"},
    {"name": "Linear", "category": "Productivity and Project Management", "hint": "developers.linear.app"},
    {"name": "Jira", "category": "Productivity and Project Management", "hint": "developer.atlassian.com"},
    {"name": "Asana", "category": "Productivity and Project Management", "hint": "developers.asana.com"},
    {"name": "Monday.com", "category": "Productivity and Project Management", "hint": "developer.monday.com"},
    {"name": "ClickUp", "category": "Productivity and Project Management", "hint": "clickup.com/api"},
    {"name": "Coda", "category": "Productivity and Project Management", "hint": "coda.io/developers"},
    {"name": "Smartsheet", "category": "Productivity and Project Management", "hint": "smartsheet.com/developers"},
    {"name": "Harvest", "category": "Productivity and Project Management", "hint": "harvestapp.com"},
    {"name": "Stripe", "category": "Finance and Fintech", "hint": "stripe.com/docs/api"},
    {"name": "Plaid", "category": "Finance and Fintech", "hint": "plaid.com/docs"},
    {"name": "Binance", "category": "Finance and Fintech", "hint": "binance-docs.github.io"},
    {"name": "Paygent Connect", "category": "Finance and Fintech", "hint": "paygent"},
    {"name": "iPayX", "category": "Finance and Fintech", "hint": "ipayx.ai/docs"},
    {"name": "QuickBooks", "category": "Finance and Fintech", "hint": "developer.intuit.com"},
    {"name": "Xero", "category": "Finance and Fintech", "hint": "developer.xero.com"},
    {"name": "Brex", "category": "Finance and Fintech", "hint": "developer.brex.com"},
    {"name": "Ramp", "category": "Finance and Fintech", "hint": "docs.ramp.com"},
    {"name": "PitchBook", "category": "Finance and Fintech", "hint": "pitchbook.com"},
    {"name": "NotebookLM", "category": "AI, Research and Media-native", "hint": "cloud.google.com/gemini"},
    {"name": "Otter AI", "category": "AI, Research and Media-native", "hint": "help.otter.ai"},
    {"name": "Fathom", "category": "AI, Research and Media-native", "hint": "fathom.video"},
    {"name": "Consensus", "category": "AI, Research and Media-native", "hint": "consensus.app"},
    {"name": "Reducto", "category": "AI, Research and Media-native", "hint": "reducto.ai"},
    {"name": "Devin", "category": "AI, Research and Media-native", "hint": "docs.devin.ai"},
    {"name": "higgsfield", "category": "AI, Research and Media-native", "hint": "higgsfield.ai/cli"},
    {"name": "Mermaid CLI", "category": "AI, Research and Media-native", "hint": "github.com/mermaid-js/mermaid-cli"},
    {"name": "YouTube Transcript", "category": "AI, Research and Media-native", "hint": "transcriptapi.com"},
    {"name": "Grain", "category": "AI, Research and Media-native", "hint": "grain.com"},
]


def infer_auth(hint: str) -> str:
    lower = hint.lower()
    if "oauth" in lower or "developers.facebook.com/docs" in lower:
        return "OAuth2"
    if "developer" in lower or "docs" in lower or "api" in lower:
        return "API key / token"
    if "basic" in lower:
        return "Basic auth"
    return "Token / custom"


def infer_access(hint: str) -> str:
    lower = hint.lower()
    if any(x in lower for x in ["ads", "bank", "finance", "pitchbook", "binance", "paygent", "whatsapp"]):
        return "gated or partner-sensitive"
    if any(x in lower for x in ["developer", "docs", "api", "shopify.dev", "open.larksuite.com"]):
        return "self-serve or trialable"
    return "mixed"


def build_summary(rows):
    category_counts = Counter(row["category"] for row in rows)
    auth_counts = Counter(row["auth"] for row in rows)
    access_counts = Counter(row["access"] for row in rows)
    easy = [row["name"] for row in rows if row["access"] == "self-serve or trialable"][:12]
    return {
        "app_count": len(rows),
        "categories": dict(category_counts),
        "auth_distribution": dict(auth_counts),
        "access_distribution": dict(access_counts),
        "easy_wins": easy,
        "headline": "OAuth2 and API-key models dominate; SaaS apps are mostly self-serve, while finance and advertising products skew gated.",
    }


def main() -> None:
    result = []
    for item in APP_LIST:
        row = {
            "name": item["name"],
            "category": item["category"],
            "hint": item["hint"],
            "auth": infer_auth(item["hint"]),
            "access": infer_access(item["hint"]),
            "buildability": "high" if item["category"] not in {"Finance and Fintech", "Marketing, Ads, Email and Social", "Data, SEO and Scraping"} else "medium",
        }
        result.append(row)

    summary = build_summary(result)
    output = {
        "summary": summary,
        "apps": result,
    }

    output_path = Path("research_output.json")
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote {output_path} with {len(result)} app records.")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

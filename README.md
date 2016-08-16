Confluence to Deveo converter
============================

# Motivation

Deveo is a code hosting and collaboration platform that has a git powered Wiki. The Wiki utilizes markdown formatting. The purpose of this project is to allow easy migration from existing Confluence space to Deveo Wiki.

# What it does

This tool will migrate the latest version of a Confluence space to Markdown files that can be used in any Markdown based Wiki. The following are migrated:
- Links
- Formatting
- Pages
- Attachments

# What it does not

- Migrate the page history
- Distinguish between attachments that have same name but have been attached to different pages. 

# Requirements

In order to execute the migration, you need to have at least the following:
- Java (I used 1.8.0_60)
- Python (I used 2.7.10)

# Instructions

1. Clone the repository:
```
git clone --recursive https://github.com/Deveo/confluence-to-deveo-converter.git
```

2. Execute the python script in the folder it is:
```
python confluence-deveo.py [CONFLUENCE_URL] [CONFLUENCE_SPACE_KEY] [CONFLUENCE_USER] [CONFLUENCE_PASSWORD]
```
, where:
- [CONFLUENCE_UR] is the url of your confluence installation, e.g. `https://confluence.domain.com/`,
- [CONFLUENCE_SPACE_KEY] is the space you wish to migrate, e.g. `MYSPACE`, 
- [CONFLUENCE_USER] is your confluence user name that has permission to read the space and its pages, e.g. `ikontulainen`, and
- [CONFLUENCE_PASSWORD] is password for your confluence user.

# More information

If you would like to read more about the migration process, check [this blog post](http://blog.deveo.com/confluence-to-markdown-wiki-migration)

If you would like to know more about Deveo: visit [our homepage](https://deveo.com)

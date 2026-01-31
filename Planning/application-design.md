# News Application – System Design

## Overview
This is a Django-based news application that allows journalists to create articles, editors or publishers to approve them, and readers to consume approved content through both the web interface and a RESTful API.

## User Roles
- Reader: Subscribes to publishers or journalists and consumes approved articles and independent articles.
- Journalist: Creates articles
- Publisher: Represents an organisation whose articles can be subscribed to

## Application Architecture
- Backend Framework: Django 6.0
- API Framework: Django REST Framework
- Database: MySQL 
- Authentication: Django authentication with a custom User model
- Rendering Formats: JSON and XML

## Installed Domain Apps
- users: Custom user model and authentication
- articles: Article creation and approval state
- publishers: Publisher entities
- subscriptions: Reader subscriptions to journalists or publishers
- api: Read-only REST API endpoints

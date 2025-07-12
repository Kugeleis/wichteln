# Services API Reference

The services layer contains the core business logic and external integrations.

## App Factory

Application factory and service initialization for the Secret Santa application.

::: services.app_factory

## Debug Logger

Debug logging utilities for the Secret Santa application.

This module provides centralized debug logging functionality
to help with development and troubleshooting.

::: services.debug_logger

## Email Service

Email service functionality for the Secret Santa application.

Refactored to use single responsibility functions for better maintainability.

::: services.email_service

## Email Templates

Email template utilities for the Secret Santa application.

This module provides utilities for creating email content and templates
for different types of notifications.

::: services.email_templates

## Recaptcha Service

reCAPTCHA verification service for the Secret Santa application.

::: services.recaptcha_service

## Request Handler

Request handling utilities for the Secret Santa application.

This module provides common utilities for processing form requests,
handling validation, and managing flash messages.

::: services.request_handler

## Token Manager

Token management utilities for the Secret Santa application.

This module provides utilities for generating, storing, and managing
confirmation tokens for assignment operations. Each class has a single
responsibility following the SRP principle.

::: services.token_manager

## Validators

Business logic validators for the Secret Santa application.

This module provides reusable validation functions for business rules
and constraints specific to the Secret Santa game.

::: services.validators

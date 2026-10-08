# Software writing examples

These examples show clearer wording without changing responsibilities, requirements, or evidence.

## Documentation: conditions and actions

Before:

> In the event that `CACHE_ENABLED` is set to `true`, you must restart the worker after changing `CACHE_TTL` to ensure that the new value is loaded, except when the worker has not yet started.

After:

> If `CACHE_ENABLED` is `true` and the worker is running, you must restart the worker after changing `CACHE_TTL`. The restart loads the new value. If the worker has not started, a restart is not required.

The condition, exception, command identifiers, and requirement strength remain intact. Do not shorten this to “Restart the worker after changing the cache settings”; that loses the condition and broadens the affected settings.

## Documentation: one action per step

Before:

> Before you restart the service, run `tool config validate`, and then restart the service with `tool service restart` only if validation succeeds.

After:

> 1. Run `tool config validate`.
> 2. If validation succeeds, run `tool service restart`.

The commands, order, and success condition remain exact.

## PR: preserve uncertainty and limits

Before:

> This change facilitates the prevention of duplicate sends by having the worker check the stored delivery ID when a job is retried after a timeout, although sends may still be duplicated if the provider accepts a request before the delivery ID is stored. The unit tests passed, but the provider integration has not been tested.

After:

> When a job retries after a timeout, the worker checks the stored delivery ID to prevent duplicate sends. Duplicates remain possible if the provider accepts a request before the delivery ID is stored. Unit tests passed. The provider integration has not been tested.

Do not turn the qualified behavior into “Retries never send duplicate messages,” or describe the untested integration as verified.

## Ticket: preserve requirement strength

Before:

> Administrators should be able to export the audit log, and exports must exclude events older than 90 days. Support users may request an export from an administrator.

After:

> Administrators should be able to export the audit log. Exports must exclude events older than 90 days. Support users may request an export from an administrator.

Keep `should`, `must`, and `may`. Changing every sentence to `must` would create requirements the source does not contain.

## Review: ambiguity needs evidence

Source:

> When the worker notifies the scheduler, it must clear the pending flag unless the retry limit is reached.

Review:

> “It” could mean the worker or the scheduler. Identify which component clears the pending flag. Keep the retry-limit exception attached to that action.

A rewrite can retain the source sentence while editing surrounding text. Do not choose an actor without evidence, or remove the exception to make the sentence shorter.

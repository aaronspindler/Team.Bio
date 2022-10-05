def traces_sampler(sampling_context):
    # Examine provided context data (including parent decision, if any)
    # along with anything in the global namespace to compute the sample rate
    # or sampling decision for this transaction

    wsgi_env = sampling_context.get("wsgi_environ")

    # If the WSGI environment is available, you can use it to determine which endpoint was called
    # We do not want to track /admin since it is being used as healthcheck endpoint
    sample_rate = 1.0
    if wsgi_env:
        path = wsgi_env.get("PATH_INFO")
        ignore_paths = [
            "/system/health",
            "/system/health/",
        ]
        if path in ignore_paths:
            sample_rate = 0.0
    return sample_rate
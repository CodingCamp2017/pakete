package com.itestra.codingcamp.androidpost.rest;

import com.itestra.codingcamp.androidpost.exceptions.RestException;

import org.json.JSONObject;

/**
 * This is a helper class that allows "throwing" Exceptions in AsyncTask that is received by a different Thread via getError()
 *
 */

public class AsyncTaskResult {
    private JSONObject result;
    private RestException error;

    public JSONObject getResult() throws RestException {
        if (hasError()) {
            throw getError();
        }
        return result;
    }

    public RestException getError() {
        return error;
    }

    public boolean hasError() {
        return getError() != null;
    }

    public AsyncTaskResult() { //empty result but no error
        super();
    }

    public AsyncTaskResult(JSONObject result) {
        super();
        this.result = result;
    }

    public AsyncTaskResult(RestException error) {
        super();
        this.error = error;
    }
}
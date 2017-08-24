package com.itestra.codingcamp.androidpost.rest;

import com.itestra.codingcamp.androidpost.exceptions.RestException;

/**
 * This is a helper class that allows "throwing" Exceptions in AsyncTask that is received by a different Thread via getError()
 *
 */

public class AsyncTaskResult<T> {
    private T result;
    private RestException error;

    public T getResult() {
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

    public AsyncTaskResult(T result) {
        super();
        this.result = result;
    }

    public AsyncTaskResult(RestException error) {
        super();
        this.error = error;
    }
}
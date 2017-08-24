package com.itestra.codingcamp.androidpost.rest;

import com.itestra.codingcamp.androidpost.exceptions.RestException;

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

    public AsyncTaskResult(T result) {
        super();
        this.result = result;
    }

    public AsyncTaskResult(RestException error) {
        super();
        this.error = error;
    }
}
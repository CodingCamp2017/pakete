package com.itestra.codingcamp.androidpost.exceptions;

/**
 * Created by simon on 24.08.17.
 */

public class KeyNotFoundException extends RestException {
    private String key;

    public KeyNotFoundException(String key, String message) {
        super(message);
        this.key = key;
    }

    public String getKey() {
        return this.key;
    }
}

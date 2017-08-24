package com.itestra.codingcamp.androidpost.exceptions;

/**
 * Created by simon on 24.08.17.
 */

public class ResourceNotFoundException extends RestException{
    String id = null;

    public ResourceNotFoundException(String id, String message) {
        super(message);
        this.id = id;
    }

    public String getId() {
        return this.id;
    }
}

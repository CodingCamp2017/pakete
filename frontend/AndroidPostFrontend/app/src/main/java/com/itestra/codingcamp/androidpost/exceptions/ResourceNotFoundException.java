package com.itestra.codingcamp.androidpost.exceptions;

/**
 * Created by simon on 24.08.17.
 */

public class ResourceNotFoundException extends RestException{

    public ResourceNotFoundException() {
        super("Resource not found");
    }
}

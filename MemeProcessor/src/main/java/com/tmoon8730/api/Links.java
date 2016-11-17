package com.tmoon8730.api;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Links {
	private Self self;

	/**
	 * @return the self
	 */
	public Self getSelf() {
		return self;
	}

	/**
	 * @param self the self to set
	 */
	public void setSelf(Self self) {
		this.self = self;
	}

	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "Links [self=" + self + "]";
	}
}

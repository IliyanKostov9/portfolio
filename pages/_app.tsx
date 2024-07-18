'use client';

import "@/styles/app.css";
import type { AppProps } from "next/app";
import { Amplify } from "aws-amplify";
import type { WithAuthenticatorProps } from "@aws-amplify/ui-react";
import { withAuthenticator } from "@aws-amplify/ui-react";
import outputs from "@/amplify_outputs.json";
import "@aws-amplify/ui-react/styles.css";

Amplify.configure(outputs, {
	ssr: true
});



function App({ Component, pageProps, signOut, user }: WithAuthenticatorProps) {
	return (
		<>
			<h1>Hello {user?.username}</h1>
			<button onClick={signOut}>Sign out</button>
			<Component {...pageProps} />
		</>
	);
}

export default withAuthenticator(App);


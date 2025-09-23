# Portfolio Website

A modern portfolio website built with React and deployed on Netlify.

## Features

- Responsive design
- Contact form with email notifications via Netlify Forms
- Portfolio sections for projects, skills, experience, etc.

## Setup

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   yarn install
   ```

3. Start the development server:
   ```
   yarn start
   ```

4. Build for production:
   ```
   yarn build
   ```

## Netlify Forms Setup

This project uses Netlify Forms to handle the contact form submissions. When someone submits the form, you'll receive an email notification.

### How it works:

1. The contact form is pre-rendered in the HTML to ensure Netlify detects it during build time
2. Form submissions are handled by Netlify's form processing service
3. Email notifications are sent to the site owner (you) when someone submits the form

### To enable email notifications:

1. Deploy your site to Netlify
2. Go to your Netlify dashboard > Site settings > Forms
3. Verify that the "portfolio-contact" form is detected
4. Go to Form notifications > Add notification > Email notification
5. Enter your email address and customize the notification settings
6. Save the notification settings

Now you'll receive an email whenever someone submits the contact form on your portfolio website.

## Deployment

This site is configured to deploy on Netlify. Simply push to your connected repository, and Netlify will automatically build and deploy your site.

The `netlify.toml` file includes all necessary configuration for deployment and form handling.

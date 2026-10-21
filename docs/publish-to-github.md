# Publish this sample to your GitHub account

1. Sign in at https://github.com/new.
2. Create a **public** repository named `repository-validation-llm-evaluation`. Do not initialize it with a README, `.gitignore`, or license; this folder already contains them.
3. Unzip this project and open PowerShell in the extracted project folder.
4. Run these commands, replacing `YOUR-USERNAME` with your GitHub username:

```powershell
git init
git add .
git commit -m "Add repository validation portfolio sample"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/repository-validation-llm-evaluation.git
git push -u origin main
```

If Git is not installed or configured, you can create the repository on GitHub, choose **Add file → Upload files**, and upload the extracted project files instead.

Before publishing, check that the README clearly labels this as a self-authored portfolio exercise. Do not describe it as a production incident, upstream contribution, paid project, or measured LLM benchmark. Run the setup yourself so you can explain the code and results during an interview.

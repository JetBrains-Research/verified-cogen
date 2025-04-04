import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.buildSteps.python
import jetbrains.buildServer.configs.kotlin.buildSteps.script
import jetbrains.buildServer.configs.kotlin.triggers.vcs
import jetbrains.buildServer.configs.kotlin.vcs.GitVcsRoot

version = "2024.12"

project {
    vcsRoot(HttpsGithubComJetBrainsResearchVerifiedCogenRefsHeadsMain)

    buildType(Build)
}

object Build : BuildType({
    name = "Build"

    vcs {
        root(HttpsGithubComJetBrainsResearchVerifiedCogenRefsHeadsMain)
    }

    params {
        password("env.GRAZIE_JWT_TOKEN", "credentialsJSON:1965ecbb-d8a2-404c-bbbd-1a1b80f733d8")
        text("env.VERIFIER_COMMAND", "dafny verify --verification-time-limit 20", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text("directory", "benches/HumanEval-Dafny", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text("llm-profile", "anthropic-claude-3.7-sonnet", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text(
            "prompts",
            "prompts/dafny_eval,prompts/dafny_eval,prompts/dafny_eval_comment_without_impls,prompts/dafny_eval_comment_without_impls_textd,prompts/dafny_eval_comment_without_impls_textd,prompts/dafny_eval_comment_without_impls_textd",
            display = ParameterDisplay.PROMPT,
            allowEmpty = false
        )
        text("extension", "dfy", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text("bench-types", "validating,validating,validating,validating,validating,validating", display = ParameterDisplay.PROMPT, allowEmpty = false)
    }

    steps {
        python {
            environment = poetry { }
            command = module {
                module = "verified_cogen"
                scriptArguments = """--insert-conditions-mode=llm-single-step
                    --llm-profile=%llm-profile%
                    --bench-types=%bench-types%
                    --tries 10
                    --runs 5
                    --filter-by-ext %extension%
                    --output-logging
                    --dir %directory%
                    --modes=mode1,mode2,mode3,mode4,mode5,mode6
                    --prompts-directory=%prompts%
                """.trimIndent().replace("\n", " ")
            }
            dockerImage = "weethet/verified-cogen:latest"
        }
    }

    artifactRules = """
        results/** => results.zip
        -:results/archive/**
    """.trimIndent()
})

object HttpsGithubComJetBrainsResearchVerifiedCogenRefsHeadsMain : GitVcsRoot({
    name = "https://github.com/JetBrains-Research/verified-cogen#refs/heads/main"
    url = "https://github.com/JetBrains-Research/verified-cogen"
    branch = "refs/heads/main"
    branchSpec = "refs/heads/*"
    authMethod = password {
        userName = "WeetHet"
        password = "credentialsJSON:75f50a52-aad8-4471-b408-a43fbd2d0b79"
    }
})

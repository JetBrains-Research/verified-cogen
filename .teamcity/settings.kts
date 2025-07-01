import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.buildSteps.python
import jetbrains.buildServer.configs.kotlin.buildSteps.script
import jetbrains.buildServer.configs.kotlin.triggers.vcs
import jetbrains.buildServer.configs.kotlin.vcs.GitVcsRoot

version = "2025.03"

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
        password("env.GRAZIE_JWT_TOKEN", "%grazie.token%")
        // text("env.VERIFIER_COMMAND", "dafny verify --verification-time-limit 20", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text("env.VERIFIER_COMMAND", "rm -rf .mypy_cache; nagini", display = ParameterDisplay.PROMPT, allowEmpty = false)
        // text("directory", "benches/HumanEval-Dafny", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text("directory", "benches/HumanEval-Nagini/Bench", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text("llm-profile", "anthropic-claude-3.7-sonnet", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text(
            "prompts",
            // "prompts/dafny_eval,prompts/dafny_eval,prompts/dafny_eval_comment_without_impls,prompts/dafny_eval_comment_without_impls_textd,prompts/dafny_eval_comment_without_impls_textd,prompts/dafny_eval_comment_without_impls_textd",
            "prompts/humaneval-nagini-few-shot,prompts/humaneval-nagini-without-conditions-few-shot,prompts/humaneval-nagini-without-impls-few-shot,prompts/humaneval-nagini-without-impls-few-shot-text-description,prompts/humaneval-nagini-without-impls+conditions-few-shot,prompts/humaneval-nagini-without-helpers-few-shot",
            display = ParameterDisplay.PROMPT,
            allowEmpty = false
        )
        // text("extension", "dfy", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text("extension", "py", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text("bench-types", "validating,validating,validating,validating,validating,validating", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text("temperature", "0.0", display = ParameterDisplay.PROMPT, allowEmpty = false)
        text("manual-rewriters", "", display = ParameterDisplay.PROMPT, allowEmpty = true)
        text("max-jobs", "10", display = ParameterDisplay.PROMPT, allowEmpty = false)
    }

    steps {
//        script {
//            scriptContent = "docker build . -t verified-cogen:latest"
//        }

        python {
            environment = poetry { }
            command = module {
                module = "verified_cogen"

                val manualRewriters = "%manual-rewriters%"
                val manualRewritersArg = if (!manualRewriters.isNullOrBlank()) {
                    "--manual-rewriters $manualRewriters"
                } else {
                    ""
                }

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
                    --temperature=%temperature%
                    --max-jobs=%max-jobs%
                    $manualRewritersArg
                """.trimIndent().replace("\n", " ")
            }
            dockerImage = "alex28sh/verus-env:latest"
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
        userName = "alex28sh"
        password = "%github.token%"
    }
})

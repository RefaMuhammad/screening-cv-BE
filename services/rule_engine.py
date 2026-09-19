from models.schemas import JobRequirement, CandidateInfo, Gate1Result, Gate1Criteria, CriteriaResult

class RuleEngine:
    def evaluate(self, candidate: CandidateInfo, job: JobRequirement, filename: str) -> Gate1Result:
        
        # 1. Experience Check
        exp_req = job.candidate_requirements.minimum_experience_years
        exp_actual = candidate.total_relevant_experience_years
        
        if exp_actual is None:
            exp_res = CriteriaResult(
                status="REVIEW", 
                required=f"Minimum {exp_req} years", 
                actual="Unknown (Missing start dates)", 
                reason="Experience duration could not be calculated because the CV is missing start dates."
            )
        elif exp_actual >= exp_req:
            exp_res = CriteriaResult(status="PASS", required=f"Minimum {exp_req} years", actual=f"{exp_actual} years", reason="Candidate meets minimum experience requirement")
        else:
            exp_res = CriteriaResult(status="FAIL", required=f"Minimum {exp_req} years", actual=f"{exp_actual} years", reason="Candidate experience is below requirement")

        # 2. Skills Check
        mandatory_skills = [s.name.lower() for s in job.candidate_requirements.skills if s.mandatory]
        candidate_skills = [s.lower() for s in candidate.skills]
        
        matched_skills = [s for s in mandatory_skills if any(s in cs or cs in s for cs in candidate_skills)]
        missing_skills = [s for s in mandatory_skills if s not in matched_skills]
        
        if not mandatory_skills:
            skill_res = CriteriaResult(status="PASS", required="None", actual="N/A", reason="No mandatory skills required")
        elif not missing_skills:
            skill_res = CriteriaResult(status="PASS", required=", ".join(mandatory_skills), actual=", ".join(matched_skills), reason="All mandatory skills matched")
        elif len(matched_skills) > 0:
            skill_res = CriteriaResult(status="REVIEW", required=", ".join(mandatory_skills), actual=f"Matched: {', '.join(matched_skills)}. Missing: {', '.join(missing_skills)}", reason="Partial skills match")
        else:
            skill_res = CriteriaResult(status="FAIL", required=", ".join(mandatory_skills), actual="None", reason="No mandatory skills matched")

        # 3. Language Check (with CEFR hierarchy)
        cefr_map = {"a1": 1, "a2": 2, "b1": 3, "b2": 4, "c1": 5, "c2": 6, "native": 7}
        req_langs = job.candidate_requirements.language_requirements
        
        lang_res = CriteriaResult(status="REVIEW", required="Unknown", actual="Unknown", reason="Language status unclear")
        if req_langs:
            req_lang = req_langs[0].language.lower()
            req_level_str = req_langs[0].minimum_level.lower()
            req_score = cefr_map.get(req_level_str, 0)
            
            # Find candidate's matching language
            cand_lang_obj = next((l for l in candidate.languages if l.language.lower() == req_lang), None)
            
            if cand_lang_obj:
                cand_level_str = cand_lang_obj.level.lower()
                cand_score = cefr_map.get(cand_level_str, 0)
                
                if cand_score >= req_score:
                    lang_res = CriteriaResult(status="PASS", required=f"{req_langs[0].language} ({req_langs[0].minimum_level})", actual=f"{cand_lang_obj.language} ({cand_lang_obj.level})", reason="Candidate meets or exceeds language proficiency")
                else:
                    lang_res = CriteriaResult(status="FAIL", required=f"{req_langs[0].language} ({req_langs[0].minimum_level})", actual=f"{cand_lang_obj.language} ({cand_lang_obj.level})", reason="Candidate proficiency is below requirement")
            else:
                lang_res = CriteriaResult(status="REVIEW", required=f"{req_langs[0].language} ({req_langs[0].minimum_level})", actual="Not found explicitly", reason="Required language not explicitly mentioned")
        else:
            lang_res = CriteriaResult(status="PASS", required="None", actual="N/A", reason="No language requirement")

        # 4. Visa Check
        visa_req = job.candidate_requirements.visa_requirement
        visa_actual = (candidate.visa_status or "unknown").lower()
        
        if visa_req:
            if "eligible" in visa_actual or "citizen" in visa_actual or "resident" in visa_actual:
                visa_res = CriteriaResult(status="PASS", required=visa_req, actual=candidate.visa_status, reason="Candidate appears eligible based on CV")
            elif visa_actual == "unknown":
                visa_res = CriteriaResult(status="REVIEW", required=visa_req, actual="Unknown", reason="Visa eligibility not mentioned in CV")
            else:
                visa_res = CriteriaResult(status="FAIL", required=visa_req, actual=candidate.visa_status, reason="Candidate does not meet visa requirement")
        else:
            visa_res = CriteriaResult(status="PASS", required="None", actual="N/A")

        # 5. Role Alignment Check (AI Evaluated)
        if candidate.role_alignment:
            role_res = CriteriaResult(
                status=candidate.role_alignment.status,
                required="Role Description Alignment",
                actual="AI Evaluated",
                reason=candidate.role_alignment.reason
            )
        else:
            role_res = CriteriaResult(status="REVIEW", required="Role Description Alignment", actual="N/A", reason="AI did not provide alignment evaluation")

        # Overall Status
        statuses = [exp_res.status, skill_res.status, lang_res.status, visa_res.status, role_res.status]
        
        if "FAIL" in statuses:
            overall = "FAIL"
            overall_reason = "Candidate failed one or more mandatory requirements or explicitly violated role description knockouts."
        elif "REVIEW" in statuses:
            overall = "REVIEW"
            overall_reason = "Some criteria could not be fully verified and require human review."
        else:
            overall = "PASS"
            overall_reason = "Candidate meets all requirements."

        return Gate1Result(
            candidate_name=candidate.candidate_name,
            filename=filename,
            status=overall,
            criteria=Gate1Criteria(
                experience=exp_res,
                skills=skill_res,
                language=lang_res,
                visa=visa_res,
                role_alignment=role_res
            ),
            overall_reason=overall_reason,
            evidence_snippets=candidate.evidence
        )

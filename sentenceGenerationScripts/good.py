# Based on the good behavior generator

# generating good transcripts
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
import time
import pandas as pd

client = OpenAI()

# Define profiles with both peer supporter and patient details
profiles = [
      {
        "peer_supporter": {
            "age": 35,
            "gender": "female",
            "personality_traits": "compassionate, insightful",
            "mental_health_history": "recovered from PTSD",
            "session_topic": "coping with trauma"
        },
        "patient": {
            "age": 29,
            "gender": "male",
            "personality_traits": "distrustful, struggling",
            "mental_health_issue": "trauma recovery"
        }
    },
    {
        "peer_supporter": {
            "age": 40,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "managing mood swings"
        },
        "patient": {
            "age": 24,
            "gender": "female",
            "personality_traits": "impulsive, energetic",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 28,
            "gender": "male",
            "personality_traits": "empathetic, encouraging",
            "mental_health_history": "overcame social anxiety",
            "session_topic": "building social confidence"
        },
        "patient": {
            "age": 22,
            "gender": "female",
            "personality_traits": "shy, eager to improve",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 45,
            "gender": "female",
            "personality_traits": "compassionate, patient",
            "mental_health_history": "recovered from depression",
            "session_topic": "managing depressive episodes"
        },
        "patient": {
            "age": 38,
            "gender": "male",
            "personality_traits": "withdrawn, seeking guidance",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 32,
            "gender": "female",
            "personality_traits": "motivated, supportive",
            "mental_health_history": "history of eating disorder",
            "session_topic": "healthy eating habits"
        },
        "patient": {
            "age": 27,
            "gender": "female",
            "personality_traits": "self-critical, determined",
            "mental_health_issue": "eating disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "male",
            "personality_traits": "wise, reflective",
            "mental_health_history": "overcame alcoholism",
            "session_topic": "maintaining sobriety"
        },
        "patient": {
            "age": 42,
            "gender": "male",
            "personality_traits": "regretful, hopeful",
            "mental_health_issue": "alcohol addiction"
        }
    },
    {
        "peer_supporter": {
            "age": 37,
            "gender": "female",
            "personality_traits": "positive, empathetic",
            "mental_health_history": "history of anxiety",
            "session_topic": "anxiety management"
        },
        "patient": {
            "age": 31,
            "gender": "male",
            "personality_traits": "anxious, seeking calm",
            "mental_health_issue": "generalized anxiety disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "male",
            "personality_traits": "understanding, friendly",
            "mental_health_history": "history of panic attacks",
            "session_topic": "coping with panic attacks"
        },
        "patient": {
            "age": 26,
            "gender": "female",
            "personality_traits": "nervous, looking for strategies",
            "mental_health_issue": "panic disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 34,
            "gender": "female",
            "personality_traits": "supportive, optimistic",
            "mental_health_history": "recovered from OCD",
            "session_topic": "managing obsessive thoughts"
        },
        "patient": {
            "age": 30,
            "gender": "male",
            "personality_traits": "obsessive, seeking control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 41,
            "gender": "female",
            "personality_traits": "insightful, patient",
            "mental_health_history": "history of borderline personality disorder",
            "session_topic": "emotional regulation"
        },
        "patient": {
            "age": 35,
            "gender": "female",
            "personality_traits": "unstable, wanting stability",
            "mental_health_issue": "borderline personality disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 33,
            "gender": "male",
            "personality_traits": "calm, understanding",
            "mental_health_history": "recovered from PTSD",
            "session_topic": "coping with flashbacks"
        },
        "patient": {
            "age": 29,
            "gender": "female",
            "personality_traits": "frightened, seeking reassurance",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 36,
            "gender": "female",
            "personality_traits": "positive, encouraging",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "balancing moods"
        },
        "patient": {
            "age": 28,
            "gender": "male",
            "personality_traits": "moody, looking for balance",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 42,
            "gender": "male",
            "personality_traits": "wise, supportive",
            "mental_health_history": "overcame gambling addiction",
            "session_topic": "dealing with addiction"
        },
        "patient": {
            "age": 34,
            "gender": "male",
            "personality_traits": "desperate, hopeful",
            "mental_health_issue": "gambling addiction"
        }
    },
    {
        "peer_supporter": {
            "age": 30,
            "gender": "female",
            "personality_traits": "encouraging, empathetic",
            "mental_health_history": "history of social anxiety",
            "session_topic": "improving social skills"
        },
        "patient": {
            "age": 25,
            "gender": "male",
            "personality_traits": "shy, eager to learn",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 48,
            "gender": "female",
            "personality_traits": "patient, understanding",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing hallucinations"
        },
        "patient": {
            "age": 39,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "male",
            "personality_traits": "insightful, patient",
            "mental_health_history": "overcame eating disorder",
            "session_topic": "healthy body image"
        },
        "patient": {
            "age": 27,
            "gender": "female",
            "personality_traits": "insecure, wanting change",
            "mental_health_issue": "body dysmorphic disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "female",
            "personality_traits": "understanding, supportive",
            "mental_health_history": "history of postpartum depression",
            "session_topic": "adjusting to parenthood"
        },
        "patient": {
            "age": 33,
            "gender": "female",
            "personality_traits": "overwhelmed, seeking balance",
            "mental_health_issue": "postpartum depression"
        }
    },
    {
        "peer_supporter": {
            "age": 44,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "recovered from addiction",
            "session_topic": "staying clean"
        },
        "patient": {
            "age": 38,
            "gender": "female",
            "personality_traits": "fearful, wanting support",
            "mental_health_issue": "drug addiction"
        }
    },
    {
        "peer_supporter": {
            "age": 35,
            "gender": "male",
            "personality_traits": "supportive, wise",
            "mental_health_history": "overcame depression",
            "session_topic": "finding happiness"
        },
        "patient": {
            "age": 30,
            "gender": "male",
            "personality_traits": "hopeless, searching for joy",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "female",
            "personality_traits": "patient, empathetic",
            "mental_health_history": "history of chronic pain",
            "session_topic": "coping with chronic illness"
        },
        "patient": {
            "age": 44,
            "gender": "female",
            "personality_traits": "frustrated, wanting relief",
            "mental_health_issue": "chronic pain"
        }
    },
    {
        "peer_supporter": {
            "age": 37,
            "gender": "male",
            "personality_traits": "positive, encouraging",
            "mental_health_history": "overcame PTSD",
            "session_topic": "building resilience"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "scared, seeking strength",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "empathetic, supportive",
            "mental_health_history": "history of anxiety",
            "session_topic": "coping with stress"
        },
        "patient": {
            "age": 26,
            "gender": "male",
            "personality_traits": "stressed, looking for relief",
            "mental_health_issue": "anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 43,
            "gender": "male",
            "personality_traits": "wise, reflective",
            "mental_health_history": "overcame grief",
            "session_topic": "dealing with loss"
        },
        "patient": {
            "age": 38,
            "gender": "female",
            "personality_traits": "grieving, seeking closure",
            "mental_health_issue": "grief"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "female",
            "personality_traits": "understanding, kind",
            "mental_health_history": "history of self-harm",
            "session_topic": "finding healthier coping mechanisms"
        },
        "patient": {
            "age": 28,
            "gender": "female",
            "personality_traits": "self-destructive, wanting change",
            "mental_health_issue": "self-harm"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "recovered from severe anxiety",
            "session_topic": "managing anxiety"
        },
        "patient": {
            "age": 34,
            "gender": "male",
            "personality_traits": "anxious, seeking calm",
            "mental_health_issue": "generalized anxiety disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 46,
            "gender": "female",
            "personality_traits": "patient, wise",
            "mental_health_history": "overcame depression",
            "session_topic": "finding purpose"
        },
        "patient": {
            "age": 40,
            "gender": "male",
            "personality_traits": "lost, looking for direction",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 27,
            "gender": "male",
            "personality_traits": "encouraging, empathetic",
            "mental_health_history": "history of social anxiety",
            "session_topic": "building social confidence"
        },
        "patient": {
            "age": 24,
            "gender": "female",
            "personality_traits": "shy, eager to improve",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 41,
            "gender": "male",
            "personality_traits": "insightful, supportive",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "balancing emotions"
        },
        "patient": {
            "age": 36,
            "gender": "female",
            "personality_traits": "unstable, seeking balance",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 30,
            "gender": "female",
            "personality_traits": "understanding, encouraging",
            "mental_health_history": "history of OCD",
            "session_topic": "coping with obsessive thoughts"
        },
        "patient": {
            "age": 27,
            "gender": "male",
            "personality_traits": "obsessive, seeking control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "female",
            "personality_traits": "compassionate, wise",
            "mental_health_history": "overcame PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 33,
            "gender": "female",
            "personality_traits": "fearful, wanting peace",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 45,
            "gender": "male",
            "personality_traits": "logical, patient",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing delusions"
        },
        "patient": {
            "age": 38,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 34,
            "gender": "female",
            "personality_traits": "supportive, optimistic",
            "mental_health_history": "overcame OCD",
            "session_topic": "handling compulsions"
        },
        "patient": {
            "age": 30,
            "gender": "female",
            "personality_traits": "compulsive, wanting change",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 28,
            "gender": "female",
            "personality_traits": "encouraging, empathetic",
            "mental_health_history": "history of anorexia",
            "session_topic": "developing healthy eating habits"
        },
        "patient": {
            "age": 24,
            "gender": "female",
            "personality_traits": "self-critical, determined",
            "mental_health_issue": "anorexia nervosa"
        }
    },
    {
        "peer_supporter": {
            "age": 37,
            "gender": "male",
            "personality_traits": "positive, insightful",
            "mental_health_history": "overcame depression",
            "session_topic": "finding joy"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "hopeless, seeking happiness",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "compassionate, supportive",
            "mental_health_history": "history of PTSD",
            "session_topic": "managing trauma"
        },
        "patient": {
            "age": 26,
            "gender": "male",
            "personality_traits": "struggling, looking for relief",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 33,
            "gender": "male",
            "personality_traits": "understanding, calm",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "stabilizing moods"
        },
        "patient": {
            "age": 29,
            "gender": "male",
            "personality_traits": "unstable, seeking control",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 47,
            "gender": "female",
            "personality_traits": "wise, reflective",
            "mental_health_history": "overcame grief",
            "session_topic": "coping with loss"
        },
        "patient": {
            "age": 41,
            "gender": "male",
            "personality_traits": "grieving, seeking comfort",
            "mental_health_issue": "grief"
        }
    },
    {
        "peer_supporter": {
            "age": 35,
            "gender": "male",
            "personality_traits": "supportive, wise",
            "mental_health_history": "history of addiction",
            "session_topic": "staying sober"
        },
        "patient": {
            "age": 30,
            "gender": "male",
            "personality_traits": "desperate, hopeful",
            "mental_health_issue": "substance abuse"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "female",
            "personality_traits": "encouraging, patient",
            "mental_health_history": "recovered from social anxiety",
            "session_topic": "building social skills"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "shy, wanting to improve",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 41,
            "gender": "male",
            "personality_traits": "insightful, calm",
            "mental_health_history": "history of PTSD",
            "session_topic": "coping with trauma"
        },
        "patient": {
            "age": 35,
            "gender": "male",
            "personality_traits": "struggling, seeking peace",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "female",
            "personality_traits": "understanding, supportive",
            "mental_health_history": "history of eating disorder",
            "session_topic": "healthy body image"
        },
        "patient": {
            "age": 28,
            "gender": "female",
            "personality_traits": "insecure, wanting change",
            "mental_health_issue": "body dysmorphic disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 44,
            "gender": "male",
            "personality_traits": "logical, supportive",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing symptoms"
        },
        "patient": {
            "age": 38,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "positive, supportive",
            "mental_health_history": "overcame social anxiety",
            "session_topic": "improving social interactions"
        },
        "patient": {
            "age": 26,
            "gender": "male",
            "personality_traits": "nervous, wanting confidence",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 38,
            "gender": "female",
            "personality_traits": "empathetic, understanding",
            "mental_health_history": "history of PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "fearful, seeking control",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 35,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "history of OCD",
            "session_topic": "managing compulsions"
        },
        "patient": {
            "age": 30,
            "gender": "male",
            "personality_traits": "compulsive, wanting change",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "female",
            "personality_traits": "wise, supportive",
            "mental_health_history": "overcame depression",
            "session_topic": "finding purpose"
        },
        "patient": {
            "age": 44,
            "gender": "male",
            "personality_traits": "lost, looking for direction",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 33,
            "gender": "female",
            "personality_traits": "patient, encouraging",
            "mental_health_history": "history of anorexia",
            "session_topic": "healthy eating habits"
        },
        "patient": {
            "age": 28,
            "gender": "female",
            "personality_traits": "self-critical, determined",
            "mental_health_issue": "anorexia nervosa"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "male",
            "personality_traits": "supportive, empathetic",
            "mental_health_history": "overcame PTSD",
            "session_topic": "building resilience"
        },
        "patient": {
            "age": 34,
            "gender": "female",
            "personality_traits": "struggling, wanting strength",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 27,
            "gender": "female",
            "personality_traits": "understanding, kind",
            "mental_health_history": "history of social anxiety",
            "session_topic": "improving social skills"
        },
        "patient": {
            "age": 24,
            "gender": "male",
            "personality_traits": "shy, seeking confidence",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 42,
            "gender": "male",
            "personality_traits": "logical, empathetic",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing hallucinations"
        },
        "patient": {
            "age": 36,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "female",
            "personality_traits": "encouraging, positive",
            "mental_health_history": "history of OCD",
            "session_topic": "coping with obsessive thoughts"
        },
        "patient": {
            "age": 27,
            "gender": "male",
            "personality_traits": "obsessive, seeking control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 48,
            "gender": "female",
            "personality_traits": "wise, patient",
            "mental_health_history": "history of depression",
            "session_topic": "finding joy"
        },
        "patient": {
            "age": 40,
            "gender": "female",
            "personality_traits": "hopeless, wanting happiness",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 34,
            "gender": "male",
            "personality_traits": "supportive, empathetic",
            "mental_health_history": "history of PTSD",
            "session_topic": "managing flashbacks"
        },
        "patient": {
            "age": 30,
            "gender": "female",
            "personality_traits": "frightened, seeking reassurance",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "positive, supportive",
            "mental_health_history": "overcame social anxiety",
            "session_topic": "building social confidence"
        },
        "patient": {
            "age": 26,
            "gender": "male",
            "personality_traits": "shy, wanting improvement",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 37,
            "gender": "male",
            "personality_traits": "empathetic, logical",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "balancing emotions"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "unstable, seeking balance",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 46,
            "gender": "female",
            "personality_traits": "understanding, wise",
            "mental_health_history": "history of OCD",
            "session_topic": "handling compulsions"
        },
        "patient": {
            "age": 40,
            "gender": "female",
            "personality_traits": "compulsive, wanting control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 32,
            "gender": "male",
            "personality_traits": "supportive, insightful",
            "mental_health_history": "overcame depression",
            "session_topic": "finding purpose"
        },
        "patient": {
            "age": 29,
            "gender": "female",
            "personality_traits": "lost, seeking direction",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 41,
            "gender": "female",
            "personality_traits": "patient, kind",
            "mental_health_history": "history of anorexia",
            "session_topic": "developing healthy eating habits"
        },
        "patient": {
            "age": 36,
            "gender": "female",
            "personality_traits": "self-critical, determined",
            "mental_health_issue": "anorexia nervosa"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "overcame PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 34,
            "gender": "female",
            "personality_traits": "fearful, wanting control",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 27,
            "gender": "female",
            "personality_traits": "supportive, understanding",
            "mental_health_history": "history of depression",
            "session_topic": "finding happiness"
        },
        "patient": {
            "age": 24,
            "gender": "male",
            "personality_traits": "hopeless, seeking joy",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "male",
            "personality_traits": "wise, empathetic",
            "mental_health_history": "overcame addiction",
            "session_topic": "staying sober"
        },
        "patient": {
            "age": 44,
            "gender": "female",
            "personality_traits": "desperate, hopeful",
            "mental_health_issue": "substance abuse"
        }
    },
    {
        "peer_supporter": {
            "age": 35,
            "gender": "female",
            "personality_traits": "positive, encouraging",
            "mental_health_history": "history of PTSD",
            "session_topic": "coping with flashbacks"
        },
        "patient": {
            "age": 30,
            "gender": "male",
            "personality_traits": "frightened, seeking reassurance",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "male",
            "personality_traits": "supportive, logical",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing delusions"
        },
        "patient": {
            "age": 34,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 28,
            "gender": "female",
            "personality_traits": "empathetic, encouraging",
            "mental_health_history": "history of social anxiety",
            "session_topic": "building social skills"
        },
        "patient": {
            "age": 24,
            "gender": "female",
            "personality_traits": "shy, eager to improve",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 44,
            "gender": "female",
            "personality_traits": "patient, supportive",
            "mental_health_history": "overcame depression",
            "session_topic": "finding purpose"
        },
        "patient": {
            "age": 38,
            "gender": "male",
            "personality_traits": "lost, looking for direction",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 33,
            "gender": "male",
            "personality_traits": "understanding, logical",
            "mental_health_history": "history of PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 29,
            "gender": "female",
            "personality_traits": "fearful, seeking control",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 37,
            "gender": "female",
            "personality_traits": "calm, wise",
            "mental_health_history": "overcame anxiety",
            "session_topic": "managing anxiety"
        },
        "patient": {
            "age": 32,
            "gender": "male",
            "personality_traits": "anxious, seeking calm",
            "mental_health_issue": "generalized anxiety disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "female",
            "personality_traits": "positive, supportive",
            "mental_health_history": "history of OCD",
            "session_topic": "coping with obsessive thoughts"
        },
        "patient": {
            "age": 27,
            "gender": "male",
            "personality_traits": "obsessive, seeking control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 40,
            "gender": "male",
            "personality_traits": "supportive, patient",
            "mental_health_history": "overcame social anxiety",
            "session_topic": "building social confidence"
        },
        "patient": {
            "age": 36,
            "gender": "female",
            "personality_traits": "shy, eager to improve",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 38,
            "gender": "male",
            "personality_traits": "empathetic, logical",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "balancing emotions"
        },
        "patient": {
            "age": 34,
            "gender": "female",
            "personality_traits": "unstable, seeking balance",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "positive, supportive",
            "mental_health_history": "overcame PTSD",
            "session_topic": "managing flashbacks"
        },
        "patient": {
            "age": 25,
            "gender": "male",
            "personality_traits": "frightened, seeking reassurance",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "male",
            "personality_traits": "wise, empathetic",
            "mental_health_history": "overcame addiction",
            "session_topic": "staying sober"
        },
        "patient": {
            "age": 44,
            "gender": "female",
            "personality_traits": "desperate, hopeful",
            "mental_health_issue": "substance abuse"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "female",
            "personality_traits": "patient, supportive",
            "mental_health_history": "history of OCD",
            "session_topic": "coping with compulsions"
        },
        "patient": {
            "age": 34,
            "gender": "male",
            "personality_traits": "compulsive, seeking change",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "male",
            "personality_traits": "supportive, positive",
            "mental_health_history": "overcame PTSD",
            "session_topic": "handling trauma"
        },
        "patient": {
            "age": 28,
            "gender": "female",
            "personality_traits": "struggling, wanting peace",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 42,
            "gender": "female",
            "personality_traits": "wise, encouraging",
            "mental_health_history": "history of depression",
            "session_topic": "finding joy"
        },
        "patient": {
            "age": 37,
            "gender": "female",
            "personality_traits": "hopeless, seeking happiness",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 35,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "balancing moods"
        },
        "patient": {
            "age": 30,
            "gender": "female",
            "personality_traits": "unstable, seeking stability",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 28,
            "gender": "female",
            "personality_traits": "supportive, positive",
            "mental_health_history": "history of anorexia",
            "session_topic": "healthy eating habits"
        },
        "patient": {
            "age": 24,
            "gender": "female",
            "personality_traits": "self-critical, determined",
            "mental_health_issue": "anorexia nervosa"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "female",
            "personality_traits": "empathetic, understanding",
            "mental_health_history": "history of PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "fearful, seeking control",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 41,
            "gender": "male",
            "personality_traits": "supportive, insightful",
            "mental_health_history": "overcame depression",
            "session_topic": "finding purpose"
        },
        "patient": {
            "age": 35,
            "gender": "male",
            "personality_traits": "lost, looking for direction",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 33,
            "gender": "female",
            "personality_traits": "encouraging, positive",
            "mental_health_history": "history of OCD",
            "session_topic": "coping with obsessive thoughts"
        },
        "patient": {
            "age": 28,
            "gender": "male",
            "personality_traits": "obsessive, seeking control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "female",
            "personality_traits": "wise, empathetic",
            "mental_health_history": "history of addiction",
            "session_topic": "staying clean"
        },
        "patient": {
            "age": 44,
            "gender": "male",
            "personality_traits": "desperate, hopeful",
            "mental_health_issue": "substance abuse"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "supportive, understanding",
            "mental_health_history": "history of social anxiety",
            "session_topic": "improving social skills"
        },
        "patient": {
            "age": 26,
            "gender": "female",
            "personality_traits": "shy, wanting to improve",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 45,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing hallucinations"
        },
        "patient": {
            "age": 38,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 38,
            "gender": "female",
            "personality_traits": "wise, encouraging",
            "mental_health_history": "overcame PTSD",
            "session_topic": "handling trauma"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "struggling, seeking peace",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "male",
            "personality_traits": "supportive, logical",
            "mental_health_history": "history of OCD",
            "session_topic": "coping with compulsions"
        },
        "patient": {
            "age": 27,
            "gender": "female",
            "personality_traits": "compulsive, wanting change",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 46,
            "gender": "female",
            "personality_traits": "empathetic, understanding",
            "mental_health_history": "history of depression",
            "session_topic": "finding happiness"
        },
        "patient": {
            "age": 40,
            "gender": "male",
            "personality_traits": "hopeless, seeking joy",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 35,
            "gender": "male",
            "personality_traits": "encouraging, positive",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "balancing moods"
        },
        "patient": {
            "age": 30,
            "gender": "female",
            "personality_traits": "unstable, seeking stability",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 28,
            "gender": "female",
            "personality_traits": "supportive, positive",
            "mental_health_history": "history of anorexia",
            "session_topic": "healthy eating habits"
        },
        "patient": {
            "age": 24,
            "gender": "female",
            "personality_traits": "self-critical, determined",
            "mental_health_issue": "anorexia nervosa"
        }
    },
    {
        "peer_supporter": {
            "age": 33,
            "gender": "male",
            "personality_traits": "understanding, logical",
            "mental_health_history": "history of PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 29,
            "gender": "female",
            "personality_traits": "fearful, seeking control",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 37,
            "gender": "female",
            "personality_traits": "calm, wise",
            "mental_health_history": "overcame anxiety",
            "session_topic": "managing anxiety"
        },
        "patient": {
            "age": 32,
            "gender": "male",
            "personality_traits": "anxious, seeking calm",
            "mental_health_issue": "generalized anxiety disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "female",
            "personality_traits": "wise, empathetic",
            "mental_health_history": "history of addiction",
            "session_topic": "staying clean"
        },
        "patient": {
            "age": 44,
            "gender": "male",
            "personality_traits": "desperate, hopeful",
            "mental_health_issue": "substance abuse"
        }
    },
     {
        "peer_supporter": {
            "age": 34,
            "gender": "female",
            "personality_traits": "supportive, optimistic",
            "mental_health_history": "recovered from OCD",
            "session_topic": "managing obsessive thoughts"
        },
        "patient": {
            "age": 30,
            "gender": "male",
            "personality_traits": "obsessive, seeking control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 48,
            "gender": "female",
            "personality_traits": "patient, understanding",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing hallucinations"
        },
        "patient": {
            "age": 39,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 41,
            "gender": "male",
            "personality_traits": "insightful, patient",
            "mental_health_history": "overcame eating disorder",
            "session_topic": "healthy body image"
        },
        "patient": {
            "age": 36,
            "gender": "female",
            "personality_traits": "insecure, wanting change",
            "mental_health_issue": "body dysmorphic disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "empathetic, supportive",
            "mental_health_history": "history of anxiety",
            "session_topic": "coping with stress"
        },
        "patient": {
            "age": 26,
            "gender": "male",
            "personality_traits": "stressed, looking for relief",
            "mental_health_issue": "anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 43,
            "gender": "male",
            "personality_traits": "wise, reflective",
            "mental_health_history": "overcame grief",
            "session_topic": "dealing with loss"
        },
        "patient": {
            "age": 38,
            "gender": "female",
            "personality_traits": "grieving, seeking closure",
            "mental_health_issue": "grief"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "female",
            "personality_traits": "understanding, kind",
            "mental_health_history": "history of self-harm",
            "session_topic": "finding healthier coping mechanisms"
        },
        "patient": {
            "age": 28,
            "gender": "female",
            "personality_traits": "self-destructive, wanting change",
            "mental_health_issue": "self-harm"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "recovered from severe anxiety",
            "session_topic": "managing anxiety"
        },
        "patient": {
            "age": 34,
            "gender": "male",
            "personality_traits": "anxious, seeking calm",
            "mental_health_issue": "generalized anxiety disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 46,
            "gender": "female",
            "personality_traits": "patient, wise",
            "mental_health_history": "overcame depression",
            "session_topic": "finding purpose"
        },
        "patient": {
            "age": 40,
            "gender": "male",
            "personality_traits": "lost, looking for direction",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 27,
            "gender": "male",
            "personality_traits": "encouraging, empathetic",
            "mental_health_history": "history of social anxiety",
            "session_topic": "building social confidence"
        },
        "patient": {
            "age": 24,
            "gender": "female",
            "personality_traits": "shy, eager to improve",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 41,
            "gender": "male",
            "personality_traits": "insightful, supportive",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "balancing emotions"
        },
        "patient": {
            "age": 36,
            "gender": "female",
            "personality_traits": "unstable, seeking balance",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 30,
            "gender": "female",
            "personality_traits": "understanding, encouraging",
            "mental_health_history": "history of OCD",
            "session_topic": "coping with obsessive thoughts"
        },
        "patient": {
            "age": 27,
            "gender": "male",
            "personality_traits": "obsessive, seeking control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "female",
            "personality_traits": "compassionate, wise",
            "mental_health_history": "overcame PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 33,
            "gender": "female",
            "personality_traits": "fearful, wanting peace",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 45,
            "gender": "male",
            "personality_traits": "logical, patient",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing delusions"
        },
        "patient": {
            "age": 38,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 34,
            "gender": "female",
            "personality_traits": "supportive, optimistic",
            "mental_health_history": "overcame OCD",
            "session_topic": "handling compulsions"
        },
        "patient": {
            "age": 30,
            "gender": "female",
            "personality_traits": "compulsive, wanting change",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 28,
            "gender": "female",
            "personality_traits": "encouraging, empathetic",
            "mental_health_history": "history of anorexia",
            "session_topic": "developing healthy eating habits"
        },
        "patient": {
            "age": 24,
            "gender": "female",
            "personality_traits": "self-critical, determined",
            "mental_health_issue": "anorexia nervosa"
        }
    },
    {
        "peer_supporter": {
            "age": 37,
            "gender": "male",
            "personality_traits": "positive, insightful",
            "mental_health_history": "overcame depression",
            "session_topic": "finding joy"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "hopeless, seeking happiness",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "compassionate, supportive",
            "mental_health_history": "history of PTSD",
            "session_topic": "managing trauma"
        },
        "patient": {
            "age": 26,
            "gender": "male",
            "personality_traits": "struggling, looking for relief",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 33,
            "gender": "male",
            "personality_traits": "understanding, calm",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "stabilizing moods"
        },
        "patient": {
            "age": 29,
            "gender": "male",
            "personality_traits": "unstable, seeking control",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 47,
            "gender": "female",
            "personality_traits": "wise, reflective",
            "mental_health_history": "overcame grief",
            "session_topic": "coping with loss"
        },
        "patient": {
            "age": 41,
            "gender": "male",
            "personality_traits": "grieving, seeking comfort",
            "mental_health_issue": "grief"
        }
    },
    {
        "peer_supporter": {
            "age": 35,
            "gender": "male",
            "personality_traits": "supportive, wise",
            "mental_health_history": "history of addiction",
            "session_topic": "staying sober"
        },
        "patient": {
            "age": 30,
            "gender": "male",
            "personality_traits": "desperate, hopeful",
            "mental_health_issue": "substance abuse"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "female",
            "personality_traits": "encouraging, patient",
            "mental_health_history": "recovered from social anxiety",
            "session_topic": "building social skills"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "shy, wanting to improve",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 41,
            "gender": "male",
            "personality_traits": "insightful, calm",
            "mental_health_history": "history of PTSD",
            "session_topic": "coping with trauma"
        },
        "patient": {
            "age": 35,
            "gender": "male",
            "personality_traits": "struggling, seeking peace",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "female",
            "personality_traits": "understanding, supportive",
            "mental_health_history": "history of eating disorder",
            "session_topic": "healthy body image"
        },
        "patient": {
            "age": 28,
            "gender": "female",
            "personality_traits": "insecure, wanting change",
            "mental_health_issue": "body dysmorphic disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 44,
            "gender": "male",
            "personality_traits": "logical, supportive",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing symptoms"
        },
        "patient": {
            "age": 38,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "positive, supportive",
            "mental_health_history": "overcame social anxiety",
            "session_topic": "improving social interactions"
        },
        "patient": {
            "age": 26,
            "gender": "male",
            "personality_traits": "nervous, wanting confidence",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 38,
            "gender": "female",
            "personality_traits": "empathetic, understanding",
            "mental_health_history": "history of PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "fearful, seeking control",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 35,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "history of OCD",
            "session_topic": "managing compulsions"
        },
        "patient": {
            "age": 30,
            "gender": "male",
            "personality_traits": "compulsive, wanting change",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "female",
            "personality_traits": "wise, supportive",
            "mental_health_history": "overcame depression",
            "session_topic": "finding purpose"
        },
        "patient": {
            "age": 44,
            "gender": "male",
            "personality_traits": "lost, looking for direction",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 33,
            "gender": "female",
            "personality_traits": "patient, encouraging",
            "mental_health_history": "history of anorexia",
            "session_topic": "healthy eating habits"
        },
        "patient": {
            "age": 28,
            "gender": "female",
            "personality_traits": "self-critical, determined",
            "mental_health_issue": "anorexia nervosa"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "male",
            "personality_traits": "supportive, empathetic",
            "mental_health_history": "overcame PTSD",
            "session_topic": "building resilience"
        },
        "patient": {
            "age": 34,
            "gender": "female",
            "personality_traits": "struggling, wanting strength",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 27,
            "gender": "female",
            "personality_traits": "understanding, kind",
            "mental_health_history": "history of social anxiety",
            "session_topic": "improving social skills"
        },
        "patient": {
            "age": 24,
            "gender": "male",
            "personality_traits": "shy, seeking confidence",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 42,
            "gender": "male",
            "personality_traits": "logical, empathetic",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing hallucinations"
        },
        "patient": {
            "age": 36,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "female",
            "personality_traits": "encouraging, positive",
            "mental_health_history": "history of OCD",
            "session_topic": "coping with obsessive thoughts"
        },
        "patient": {
            "age": 27,
            "gender": "male",
            "personality_traits": "obsessive, seeking control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 48,
            "gender": "female",
            "personality_traits": "wise, patient",
            "mental_health_history": "history of depression",
            "session_topic": "finding joy"
        },
        "patient": {
            "age": 40,
            "gender": "female",
            "personality_traits": "hopeless, wanting happiness",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 34,
            "gender": "male",
            "personality_traits": "supportive, empathetic",
            "mental_health_history": "history of PTSD",
            "session_topic": "managing flashbacks"
        },
        "patient": {
            "age": 30,
            "gender": "female",
            "personality_traits": "frightened, seeking reassurance",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "positive, supportive",
            "mental_health_history": "overcame social anxiety",
            "session_topic": "building social confidence"
        },
        "patient": {
            "age": 26,
            "gender": "male",
            "personality_traits": "shy, wanting improvement",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 37,
            "gender": "male",
            "personality_traits": "empathetic, logical",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "balancing emotions"
        },
        "patient": {
            "age": 32,
            "gender": "female",
            "personality_traits": "unstable, seeking balance",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 46,
            "gender": "female",
            "personality_traits": "understanding, wise",
            "mental_health_history": "history of OCD",
            "session_topic": "handling compulsions"
        },
        "patient": {
            "age": 40,
            "gender": "female",
            "personality_traits": "compulsive, wanting control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 32,
            "gender": "male",
            "personality_traits": "supportive, insightful",
            "mental_health_history": "overcame depression",
            "session_topic": "finding purpose"
        },
        "patient": {
            "age": 29,
            "gender": "female",
            "personality_traits": "lost, seeking direction",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 41,
            "gender": "female",
            "personality_traits": "patient, kind",
            "mental_health_history": "history of anorexia",
            "session_topic": "developing healthy eating habits"
        },
        "patient": {
            "age": 36,
            "gender": "female",
            "personality_traits": "self-critical, determined",
            "mental_health_issue": "anorexia nervosa"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "overcame PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 34,
            "gender": "female",
            "personality_traits": "fearful, wanting control",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 27,
            "gender": "female",
            "personality_traits": "supportive, understanding",
            "mental_health_history": "history of depression",
            "session_topic": "finding happiness"
        },
        "patient": {
            "age": 24,
            "gender": "male",
            "personality_traits": "hopeless, seeking joy",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "male",
            "personality_traits": "wise, empathetic",
            "mental_health_history": "overcame addiction",
            "session_topic": "staying sober"
        },
        "patient": {
            "age": 44,
            "gender": "female",
            "personality_traits": "desperate, hopeful",
            "mental_health_issue": "substance abuse"
        }
    },
    {
        "peer_supporter": {
            "age": 35,
            "gender": "female",
            "personality_traits": "positive, encouraging",
            "mental_health_history": "history of PTSD",
            "session_topic": "coping with flashbacks"
        },
        "patient": {
            "age": 30,
            "gender": "male",
            "personality_traits": "frightened, seeking reassurance",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "male",
            "personality_traits": "supportive, logical",
            "mental_health_history": "history of schizophrenia",
            "session_topic": "managing delusions"
        },
        "patient": {
            "age": 34,
            "gender": "male",
            "personality_traits": "confused, seeking clarity",
            "mental_health_issue": "schizophrenia"
        }
    },
    {
        "peer_supporter": {
            "age": 28,
            "gender": "female",
            "personality_traits": "empathetic, encouraging",
            "mental_health_history": "history of social anxiety",
            "session_topic": "building social skills"
        },
        "patient": {
            "age": 24,
            "gender": "female",
            "personality_traits": "shy, eager to improve",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 44,
            "gender": "female",
            "personality_traits": "patient, supportive",
            "mental_health_history": "overcame depression",
            "session_topic": "finding purpose"
        },
        "patient": {
            "age": 38,
            "gender": "male",
            "personality_traits": "lost, looking for direction",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 33,
            "gender": "male",
            "personality_traits": "understanding, logical",
            "mental_health_history": "history of PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 29,
            "gender": "female",
            "personality_traits": "fearful, seeking control",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 37,
            "gender": "female",
            "personality_traits": "calm, wise",
            "mental_health_history": "overcame anxiety",
            "session_topic": "managing anxiety"
        },
        "patient": {
            "age": 32,
            "gender": "male",
            "personality_traits": "anxious, seeking calm",
            "mental_health_issue": "generalized anxiety disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "female",
            "personality_traits": "positive, supportive",
            "mental_health_history": "history of OCD",
            "session_topic": "coping with obsessive thoughts"
        },
        "patient": {
            "age": 27,
            "gender": "male",
            "personality_traits": "obsessive, seeking control",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 40,
            "gender": "male",
            "personality_traits": "supportive, patient",
            "mental_health_history": "overcame social anxiety",
            "session_topic": "building social confidence"
        },
        "patient": {
            "age": 36,
            "gender": "female",
            "personality_traits": "shy, eager to improve",
            "mental_health_issue": "social anxiety"
        }
    },
    {
        "peer_supporter": {
            "age": 38,
            "gender": "male",
            "personality_traits": "empathetic, logical",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "balancing emotions"
        },
        "patient": {
            "age": 34,
            "gender": "female",
            "personality_traits": "unstable, seeking balance",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 29,
            "gender": "female",
            "personality_traits": "positive, supportive",
            "mental_health_history": "overcame PTSD",
            "session_topic": "managing flashbacks"
        },
        "patient": {
            "age": 25,
            "gender": "male",
            "personality_traits": "frightened, seeking reassurance",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "male",
            "personality_traits": "wise, empathetic",
            "mental_health_history": "overcame addiction",
            "session_topic": "staying sober"
        },
        "patient": {
            "age": 44,
            "gender": "female",
            "personality_traits": "desperate, hopeful",
            "mental_health_issue": "substance abuse"
        }
    },
    {
        "peer_supporter": {
            "age": 39,
            "gender": "female",
            "personality_traits": "patient, supportive",
            "mental_health_history": "history of OCD",
            "session_topic": "coping with compulsions"
        },
        "patient": {
            "age": 34,
            "gender": "male",
            "personality_traits": "compulsive, seeking change",
            "mental_health_issue": "obsessive-compulsive disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 31,
            "gender": "male",
            "personality_traits": "supportive, positive",
            "mental_health_history": "overcame PTSD",
            "session_topic": "handling trauma"
        },
        "patient": {
            "age": 28,
            "gender": "female",
            "personality_traits": "struggling, wanting peace",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 42,
            "gender": "female",
            "personality_traits": "wise, encouraging",
            "mental_health_history": "history of depression",
            "session_topic": "finding joy"
        },
        "patient": {
            "age": 37,
            "gender": "female",
            "personality_traits": "hopeless, seeking happiness",
            "mental_health_issue": "depression"
        }
    },
    {
        "peer_supporter": {
            "age": 35,
            "gender": "male",
            "personality_traits": "calm, logical",
            "mental_health_history": "history of bipolar disorder",
            "session_topic": "balancing moods"
        },
        "patient": {
            "age": 30,
            "gender": "female",


            "personality_traits": "unstable, seeking stability",
            "mental_health_issue": "bipolar disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 28,
            "gender": "female",
            "personality_traits": "supportive, positive",
            "mental_health_history": "history of anorexia",
            "session_topic": "healthy eating habits"
        },
        "patient": {
            "age": 24,
            "gender": "female",
            "personality_traits": "self-critical, determined",
            "mental_health_issue": "anorexia nervosa"
        }
    },
    {
        "peer_supporter": {
            "age": 33,
            "gender": "male",
            "personality_traits": "understanding, logical",
            "mental_health_history": "history of PTSD",
            "session_topic": "handling triggers"
        },
        "patient": {
            "age": 29,
            "gender": "female",
            "personality_traits": "fearful, seeking control",
            "mental_health_issue": "PTSD"
        }
    },
    {
        "peer_supporter": {
            "age": 37,
            "gender": "female",
            "personality_traits": "calm, wise",
            "mental_health_history": "overcame anxiety",
            "session_topic": "managing anxiety"
        },
        "patient": {
            "age": 32,
            "gender": "male",
            "personality_traits": "anxious, seeking calm",
            "mental_health_issue": "generalized anxiety disorder"
        }
    },
    {
        "peer_supporter": {
            "age": 50,
            "gender": "female",
            "personality_traits": "wise, empathetic",
            "mental_health_history": "history of addiction",
            "session_topic": "staying clean"
        },
        "patient": {
            "age": 44,
            "gender": "male",
            "personality_traits": "desperate, hopeful",
            "mental_health_issue": "substance abuse"
        }
    }
]

# System message content
system_message_content = """
You are a generator of realistic transcripts showcasing positive and effective interactions in peer-support sessions. These sessions are conducted by trained peer-supporters, not professional therapists. Your transcripts should reflect natural speaking patterns and demonstrate helpful, empathetic, and appropriate advice and support from the peer-supporter to the patient. 
Each prompt will provide details about the peer-supporter and the patient, including personality traits, gender, age, mental health history, and the topic of the session. Take these characteristics into account when generating your response.
Your role is to create a realistic portrayal of these sessions, focusing on the positive aspects and best practices that should occur in real-life peer-support interactions. Show a range of interactions that serve as examples of what to do in a peer-support session.
Keep the following guidelines in mind:
- Use natural, conversational language and sentence structure.
- Ensure each response from the peer-supporter (T) and the patient (P) is a single, complete sentence.
- Avoid filler phrases or sentences that do not contribute to the conversation's content.
- Focus on generating sentences that have a high confidence of being high fidelity in terms of the advice or support provided.
- Generate full and engaging conversations that accurately represent the complexity and variability of effective real-life peer-support interactions. 
- Allow the patient to discuss in depth their mental health problem.
"""

# Initialize a list to store profile data for later use
profile_data = []

# Loop through profiles and generate transcripts
for index, profile in enumerate(profiles, start=1):
    # Construct the prompt
    prompt = (
        f"Peer Supporter - Age: {profile['peer_supporter']['age']}, Gender: {profile['peer_supporter']['gender']}, "
        f"Traits: {profile['peer_supporter']['personality_traits']}, Mental Health History: {profile['peer_supporter']['mental_health_history']}, "
        f"Session Topic: {profile['peer_supporter']['session_topic']} \n"
        f"Patient - Age: {profile['patient']['age']}, Gender: {profile['patient']['gender']}, "
        f"Traits: {profile['patient']['personality_traits']}, Mental Health Issue: {profile['patient']['mental_health_issue']}"
    )

    # Generate transcript
    completion = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9
    )

    # Write transcript to file
    filename = f"profile_{index}_transcript.txt"
    with open(filename, "w") as file:
        file.write(completion.choices[0].message.content)  # Ensure this accesses the right property

    print(f"Transcript for Profile {index} written to file {filename}.")

    # Store profile data in a structured format
    profile_data.append({
        "profile_index": index,
        "peer_supporter_age": profile['peer_supporter']['age'],
        "peer_supporter_gender": profile['peer_supporter']['gender'],
        "peer_supporter_traits": profile['peer_supporter']['personality_traits'],
        "peer_supporter_mental_health_history": profile['peer_supporter']['mental_health_history'],
        "session_topic": profile['peer_supporter']['session_topic'],
        "patient_age": profile['patient']['age'],
        "patient_gender": profile['patient']['gender'],
        "patient_traits": profile['patient']['personality_traits'],
        "patient_mental_health_issue": profile['patient']['mental_health_issue']
    })

    time.sleep(60)  # 30-sec pause

# Convert profile data to a DataFrame
df = pd.DataFrame(profile_data)
df.to_csv("profile_data_positive_2.csv", index=False)
print("Profile data saved to profile_data_positive_2.csv")

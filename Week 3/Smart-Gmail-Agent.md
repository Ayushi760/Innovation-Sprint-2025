# Recording


[video](https://github.com/user-attachments/assets/adcc4799-8c26-4065-8ced-775d432c6782)


# Smart Gmail Agent Code:
```
{
  "name": "Ayushi Saxena",
  "nodes": [
    {
      "parameters": {
        "path": "smart-gmail-agent",
        "options": {}
      },
      "id": "b6655b0d-ee70-45f4-afed-aac89aeee91c",
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        -1380,
        220
      ],
      "webhookId": "smart-gmail-agent"
    },
    {
      "parameters": {
        "url": "https://api.escuelajs.co/api/v1/users",
        "options": {}
      },
      "id": "a4211750-ca9e-4cc0-b77c-31d9c90d2247",
      "name": "Fetch Users",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [
        -940,
        220
      ]
    },
    {
      "parameters": {
        "jsCode": "const query = $input.first().json.query || '';\n\nconst customerKeywords = [\n  \"product\", \"support\", \"sales\", \"billing\", \"feature\",\n  \"payment\", \"invoice\", \"subscription\", \"refund\", \"price\",\n  \"help\", \"plan\", \"account\", \"charge\", \"signup\", \"question\",\n  \"cancel\", \"renew\", \"upgrade\", \"downgrade\"\n];\n\nconst adminKeywords = [\n  \"escalation\", \"system\", \"security\", \"data\", \"integration\",\n  \"urgent\", \"api\", \"production\", \"incident\", \"error\",\n  \"failure\", \"outage\", \"crash\", \"bug\"\n];\n\n\nconst lowerQuery = query.query.toLowerCase();\n\nlet customerScore = 0;\nlet adminScore = 0;\n\ncustomerKeywords.forEach(keyword => {\n  if (lowerQuery.includes(keyword)) {\n    customerScore++;\n  }\n});\n\nadminKeywords.forEach(keyword => {\n  if (lowerQuery.includes(keyword)) {\n    adminScore++;\n  }\n});\n\nlet queryType = 'customer';\nif (adminScore > customerScore) {\n  queryType = 'admin';\n}\n\nif (lowerQuery.includes('urgent') || lowerQuery.includes('critical') || lowerQuery.includes('emergency')) {\n  queryType = 'admin';\n}\n\nlet category = '';\nif (queryType === 'customer') {\n  if (lowerQuery.includes('product') || lowerQuery.includes('feature')) {\n    category = 'Product Inquiry';\n  } else if (lowerQuery.includes('billing') || lowerQuery.includes('charge') || lowerQuery.includes('payment')) {\n    category = 'Billing Inquiry';\n  } else if (lowerQuery.includes('sales') || lowerQuery.includes('price') || lowerQuery.includes('plan')) {\n    category = 'Sales Question';\n  } else if (lowerQuery.includes('request')) {\n    category = 'Feature Request';\n  } else {\n    category = 'General Support';\n  }\n} else {\n  if (lowerQuery.includes('security')) {\n    category = 'Security Concern';\n  } else if (lowerQuery.includes('system') || lowerQuery.includes('server')) {\n    category = 'System Issue';\n  } else if (lowerQuery.includes('data') || lowerQuery.includes('database')) {\n    category = 'Data Issue';\n  } else if (lowerQuery.includes('integration') || lowerQuery.includes('api')) {\n    category = 'Integration Problem';\n  } else {\n    category = 'Technical Escalation';\n  }\n}\n\nreturn {\n  query: query,\n  queryType: queryType,\n  category: category,\n  customerScore: customerScore,\n  adminScore: adminScore\n};"
      },
      "id": "b2b03486-f452-42ae-83bf-580b7b05f863",
      "name": "Classify Query",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [
        -1160,
        220
      ]
    },
    {
      "parameters": {
        "jsCode": "const allInputs = $input.all();\nconst users = allInputs.map(item => item.json);\n\nconst classification = $('Classify Query').first().json;\n\nconst targetRole = classification.queryType;\nconst filteredUsers = users.filter(user => {\n  return user.role && user.role.toLowerCase() === targetRole.toLowerCase();\n});\n\nconst emailList = filteredUsers\n  .filter(user => user.email)\n  .map(user => user.email);\n\nreturn {\n  classification: classification,\n  targetRole: targetRole,\n  recipients: emailList,\n  recipientCount: emailList.length,\n  allUsers: users.length,\n  filteredUsers: filteredUsers.length\n};\n"
      },
      "id": "fe61d8c5-491e-425b-9bdf-4afb1012c880",
      "name": "Filter Users by Role",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [
        -720,
        220
      ]
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{$json.recipientCount}}",
              "operation": "larger"
            }
          ]
        }
      },
      "id": "af81696a-7baf-4652-a1e3-858497567d72",
      "name": "Recipients Exist?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        -500,
        220
      ]
    },
    {
      "parameters": {
        "jsCode": "const data = $input.first().json;\n\nconst emailSubject = `[${data.classification.category}] ${data.classification.query.query.substring(0, 50)}...`;\n\nconst emailBody = `\n<h2>New ${data.classification.queryType === 'admin' ? 'Admin' : 'Customer'} Query Received</h2>\n\n<p><strong>Category:</strong> ${data.classification.category}</p>\n<p><strong>Query Type:</strong> ${data.classification.queryType}</p>\n\n<h3>Query Content:</h3>\n<p>${data.classification.query.query}</p>\n\n<hr>\n\n<p><small>This email was automatically generated by the Smart Gmail Agent.</small></p>\n<p><small>Recipients: ${data.recipients.join(', ')}</small></p>\n`;\n\nreturn {\n  to: [\"sixovo7528@coasah.com\"],\n  subject: emailSubject,\n  html: emailBody,\n  classification: data.classification\n};"
      },
      "id": "24b826ec-e772-4e1e-9c96-5abb01da01cc",
      "name": "Prepare Email",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [
        -280,
        120
      ]
    },
    {
      "parameters": {
        "sendTo": "={{$json.to.join(',')}}",
        "subject": "={{$json.subject}}",
        "message": "={{$json.html}}",
        "options": {
          "attachmentsUi": {
            "attachmentsBinary": []
          }
        }
      },
      "id": "47daab46-79c4-496d-bf64-c90495717d71",
      "name": "Send Gmail",
      "type": "n8n-nodes-base.gmail",
      "typeVersion": 2,
      "position": [
        -60,
        120
      ],
      "webhookId": "f2413443-69f8-45c8-894d-29f28c6f2229",
      "credentials": {
        "gmailOAuth2": {
          "id": "kQS0n64PpAsf1GR5",
          "name": "Gmail account"
        }
      }
    },
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "status",
              "value": "error"
            },
            {
              "name": "message",
              "value": "No recipients found for the query type: {{$json.classification.queryType}}"
            }
          ]
        },
        "options": {}
      },
      "id": "52d2a127-c516-4230-993b-d4c7a5d43456",
      "name": "No Recipients Error",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        -280,
        320
      ]
    },
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "status",
              "value": "success"
            },
            {
              "name": "message",
              "value": "Email sent successfully"
            }
          ],
          "number": [
            {
              "name": "recipientCount",
              "value": "={{$json.to.length}}"
            }
          ]
        },
        "options": {}
      },
      "id": "ab3f4d70-adc5-4693-b0ad-01460e7e6626",
      "name": "Success Response",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        160,
        120
      ]
    }
  ],
  "pinData": {},
  "connections": {
    "Webhook Trigger": {
      "main": [
        [
          {
            "node": "Classify Query",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Fetch Users": {
      "main": [
        [
          {
            "node": "Filter Users by Role",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Classify Query": {
      "main": [
        [
          {
            "node": "Fetch Users",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Filter Users by Role": {
      "main": [
        [
          {
            "node": "Recipients Exist?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Recipients Exist?": {
      "main": [
        [
          {
            "node": "Prepare Email",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "No Recipients Error",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Prepare Email": {
      "main": [
        [
          {
            "node": "Send Gmail",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Send Gmail": {
      "main": [
        [
          {
            "node": "Success Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "c54e8d5a-1e5d-4898-8062-4d8c1293784b",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "9f4a5bda5b199c2925206155fc2cbb264c3aa429863b9500167ff248c28247d0"
  },
  "id": "2kYeXmsQjlWzaT5W",
  "tags": []
}
```
